export type TokenResponse = {
  access_token: string
  token_type: 'bearer'
}

export type PaginacionRespuesta<T> = {
  page: number
  page_size: number
  total: number
  items: T[]
}

export type TipoProductoDTO = {
  id_tipo_producto: number
  nombre: string
}

export type CrearTipoProductoDTO = {
  nombre: string
}

export type ActualizarTipoProductoDTO = {
  nombre?: string | null
}

export type BodegaDTO = {
  id_bodega: number
  nombre: string
  direccion?: string | null
}

export type CrearBodegaDTO = {
  nombre: string
  direccion?: string | null
}

export type ActualizarBodegaDTO = {
  nombre?: string | null
  direccion?: string | null
}

export type PuertoDTO = {
  id_puerto: number
  nombre: string
  ciudad?: string | null
}

export type ClienteDTO = {
  id_cliente: number
  nombre: string
  email?: string | null
  telefono?: string | null
}

export type CrearClienteDTO = {
  nombre: string
  email?: string | null
  telefono?: string | null
}

export type CrearPuertoDTO = {
  nombre: string
  ciudad?: string | null
}

export type ActualizarPuertoDTO = {
  nombre?: string | null
  ciudad?: string | null
}

export type TipoEnvio = 'TERRESTRE' | 'MARITIMO'

export type EnvioDTO = {
  id_envio: number
  id_cliente: number
  id_tipo_producto: number
  cantidad: number
  fecha_registro: string
  fecha_entrega: string
  precio_base: string
  descuento: string
  precio_final: string
  numero_guia: string
  tipo_envio: TipoEnvio
  id_bodega?: number | null
  placa_vehiculo?: string | null
  id_puerto?: number | null
  numero_flota?: string | null
}

export type CrearEnvioDTO = {
  id_cliente: number
  id_tipo_producto: number
  cantidad: number
  fecha_registro: string
  fecha_entrega: string
  precio_base: string | number
  numero_guia: string
  tipo_envio: TipoEnvio
  id_bodega?: number
  placa_vehiculo?: string
  id_puerto?: number
  numero_flota?: string
}

export type ActualizarEnvioDTO = Partial<CrearEnvioDTO>

const API_BASE = '/api/v1'

function asRecord(value: unknown): Record<string, unknown> | null {
  if (typeof value === 'object' && value !== null) return value as Record<string, unknown>
  return null
}

function safeStringify(value: unknown): string | null {
  try {
    return JSON.stringify(value)
  } catch {
    return null
  }
}

function toDisplayString(value: unknown): string {
  if (value === null || value === undefined) return ''
  if (typeof value === 'string') return value
  if (typeof value === 'number' || typeof value === 'boolean' || typeof value === 'bigint') return String(value)
  const json = safeStringify(value)
  if (json) return json
  if (typeof value === 'object') return '[unserializable]'
  if (typeof value === 'function') return '[function]'
  if (typeof value === 'symbol') return '[symbol]'
  return ''
}

function formatFastApiValidationDetail(detail: unknown): string | null {
  if (!Array.isArray(detail)) return null

  const parts = detail
    .map((entry) => {
      const rec = asRecord(entry)
      if (!rec) return String(entry)

      const locRaw = rec.loc
      let loc = ''
      if (Array.isArray(locRaw)) {
        loc = locRaw.map((p) => toDisplayString(p)).filter((s) => s.trim().length > 0).join('.')
      } else if (locRaw !== null && locRaw !== undefined) {
        loc = toDisplayString(locRaw)
      }

      const msgRaw = rec.msg ?? rec.message
      let msg = ''
      if (msgRaw !== null && msgRaw !== undefined) {
        msg = toDisplayString(msgRaw)
      } else {
        msg = safeStringify(entry) ?? String(entry)
      }

      return loc ? `${loc}: ${msg}` : msg
    })
    .filter((s) => s.trim().length > 0)

  return parts.length ? parts.join('\n') : null
}

function formatApiError(data: unknown, status: number): string {
  if (typeof data === 'string') return data

  const rec = asRecord(data)
  if (!rec) return `Error HTTP ${status}`

  if ('detail' in rec) {
    const detail = rec.detail
    if (typeof detail === 'string') return detail

    // FastAPI / Pydantic validation error: detail = [{loc, msg, ...}, ...]
    const validation = formatFastApiValidationDetail(detail)
    if (validation) return validation

    return safeStringify(detail) ?? String(detail)
  }

  return safeStringify(data) ?? `Error HTTP ${status}`
}

async function requestJson<T>(input: RequestInfo | URL, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  if (init?.headers) {
    Object.assign(headers, init.headers as any)
  }

  const resp = await fetch(input, {
    ...init,
    headers,
  })

  const text = await resp.text()
  let data: unknown = null
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = text
  }

  if (!resp.ok) {
    throw new Error(formatApiError(data, resp.status))
  }

  return data as T
}

function authHeaders(token: string): Record<string, string> {
  return token.trim() ? { Authorization: `Bearer ${token}` } : {}
}

function toQuery(params: Record<string, string | number | boolean | null | undefined>): string {
  const sp = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === '') continue
    sp.set(k, String(v))
  }
  const qs = sp.toString()
  return qs ? `?${qs}` : ''
}

export async function login(username: string, password: string): Promise<TokenResponse> {
  return requestJson<TokenResponse>(`${API_BASE}/auth/token`, {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function listarTiposProducto(
  token: string,
  params: { page?: number; page_size?: number; q?: string } = {},
): Promise<PaginacionRespuesta<TipoProductoDTO>> {
  return requestJson<PaginacionRespuesta<TipoProductoDTO>>(
    `${API_BASE}/tipos-producto${toQuery(params)}`,
    { method: 'GET', headers: authHeaders(token) },
  )
}

export async function crearTipoProducto(token: string, payload: CrearTipoProductoDTO): Promise<TipoProductoDTO> {
  return requestJson<TipoProductoDTO>(`${API_BASE}/tipos-producto`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
}

export async function eliminarTipoProducto(
  token: string,
  tipoProductoId: number,
): Promise<{ status: string }> {
  return requestJson<{ status: string }>(`${API_BASE}/tipos-producto/${tipoProductoId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  })
}

export async function listarBodegas(
  token: string,
  params: { page?: number; page_size?: number; q?: string } = {},
): Promise<PaginacionRespuesta<BodegaDTO>> {
  return requestJson<PaginacionRespuesta<BodegaDTO>>(
    `${API_BASE}/bodegas${toQuery(params)}`,
    { method: 'GET', headers: authHeaders(token) },
  )
}

export async function crearBodega(token: string, payload: CrearBodegaDTO): Promise<BodegaDTO> {
  return requestJson<BodegaDTO>(`${API_BASE}/bodegas`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
}

export async function eliminarBodega(token: string, bodegaId: number): Promise<{ status: string }> {
  return requestJson<{ status: string }>(`${API_BASE}/bodegas/${bodegaId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  })
}

export async function listarPuertos(
  token: string,
  params: { page?: number; page_size?: number; q?: string; ciudad?: string } = {},
): Promise<PaginacionRespuesta<PuertoDTO>> {
  return requestJson<PaginacionRespuesta<PuertoDTO>>(
    `${API_BASE}/puertos${toQuery(params)}`,
    { method: 'GET', headers: authHeaders(token) },
  )
}

export async function crearPuerto(token: string, payload: CrearPuertoDTO): Promise<PuertoDTO> {
  return requestJson<PuertoDTO>(`${API_BASE}/puertos`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
}

export async function eliminarPuerto(token: string, puertoId: number): Promise<{ status: string }> {
  return requestJson<{ status: string }>(`${API_BASE}/puertos/${puertoId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  })
}

export async function listarClientes(
  token: string,
  params: { page?: number; page_size?: number; q?: string; email?: string } = {},
): Promise<PaginacionRespuesta<ClienteDTO>> {
  return requestJson<PaginacionRespuesta<ClienteDTO>>(
    `${API_BASE}/clientes${toQuery(params)}`,
    { method: 'GET', headers: authHeaders(token) },
  )
}

export async function crearCliente(token: string, payload: CrearClienteDTO): Promise<ClienteDTO> {
  return requestJson<ClienteDTO>(`${API_BASE}/clientes`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
}

export async function eliminarCliente(token: string, clienteId: number): Promise<{ status: string }> {
  return requestJson<{ status: string }>(`${API_BASE}/clientes/${clienteId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  })
}

export async function listarEnvios(
  token: string,
  params: {
    page?: number
    page_size?: number
    q?: string
    id_cliente?: number
    id_tipo_producto?: number
    tipo_envio?: TipoEnvio
  } = {},
): Promise<PaginacionRespuesta<EnvioDTO>> {
  return requestJson<PaginacionRespuesta<EnvioDTO>>(`${API_BASE}/envios${toQuery(params as any)}`, {
    method: 'GET',
    headers: authHeaders(token),
  })
}

export async function crearEnvio(token: string, payload: CrearEnvioDTO): Promise<EnvioDTO> {
  return requestJson<EnvioDTO>(`${API_BASE}/envios`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
}

export async function eliminarEnvio(token: string, envioId: number): Promise<{ status: string }> {
  return requestJson<{ status: string }>(`${API_BASE}/envios/${envioId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  })
}
