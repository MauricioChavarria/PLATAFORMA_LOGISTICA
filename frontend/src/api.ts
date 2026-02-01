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

export type ClienteDTO = {
  id: number
  nombre: string
  email: string
  documento: string
  telefono?: string | null
  creado_en: string
}

export type CrearClienteDTO = {
  nombre: string
  email: string
  documento: string
  telefono?: string | null
}

export type ActualizarClienteDTO = {
  nombre?: string | null
  email?: string | null
  documento?: string | null
  telefono?: string | null
}

export type ProductoDTO = {
  id: number
  nombre: string
  descripcion?: string | null
  creado_en: string
}

export type CrearProductoDTO = {
  nombre: string
  descripcion?: string | null
}

export type ActualizarProductoDTO = {
  nombre?: string | null
  descripcion?: string | null
}

export type BodegaDTO = {
  id: number
  nombre: string
  ubicacion: string
  pais: string
  creado_en: string
}

export type CrearBodegaDTO = {
  nombre: string
  ubicacion: string
  pais: string
}

export type ActualizarBodegaDTO = {
  nombre?: string | null
  ubicacion?: string | null
  pais?: string | null
}

export type PuertoDTO = {
  id: number
  nombre: string
  pais: string
  creado_en: string
}

export type CrearPuertoDTO = {
  nombre: string
  pais: string
}

export type ActualizarPuertoDTO = {
  nombre?: string | null
  pais?: string | null
}

export type TipoEnvio = 'TERRESTRE' | 'MARITIMO'

export type EnvioDTO = {
  id: number
  cliente_id: number
  producto_id: number
  cantidad: number
  fecha_registro: string
  fecha_entrega: string
  precio_base: string
  descuento: string
  precio_final: string
  numero_guia: string
  tipo_envio: TipoEnvio
  bodega_id?: number | null
  placa_vehiculo?: string | null
  puerto_id?: number | null
  numero_flota?: string | null
  creado_en: string
}

export type CrearEnvioDTO = {
  cliente_id: number
  producto_id: number
  cantidad: number
  fecha_registro: string
  fecha_entrega: string
  precio_base: string | number
  descuento: string | number
  numero_guia: string
  tipo_envio: TipoEnvio
  bodega_id?: number
  placa_vehiculo?: string
  puerto_id?: number
  numero_flota?: string
}

export type ActualizarEnvioDTO = Partial<CrearEnvioDTO>

export type CotizacionTerrestreRequest = {
  guia: string
  cliente_id: number
  placa_vehiculo: string
  codigo_flota: string
  cantidad: number
}

export type CotizacionMaritimaRequest = {
  guia: string
  cliente_id: number
  puerto_origen_id: number
  puerto_destino_id: number
  cantidad: number
}

const API_BASE = '/api/v1'

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
    const message =
      typeof data === 'object' && data && 'detail' in (data as any)
        ? String((data as any).detail)
        : `Error HTTP ${resp.status}`

    throw new Error(message)
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

export async function cotizarTerrestre(
  token: string,
  payload: CotizacionTerrestreRequest,
): Promise<any> {
  return requestJson<any>(`${API_BASE}/envios/terrestres/cotizar`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  })
}

export async function cotizarMaritimo(
  token: string,
  payload: CotizacionMaritimaRequest,
): Promise<any> {
  return requestJson<any>(`${API_BASE}/envios/maritimos/cotizar`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  })
}

export async function listarClientes(
  token: string,
  params: { page?: number; page_size?: number; q?: string; email?: string; documento?: string } = {},
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

export async function listarProductos(
  token: string,
  params: { page?: number; page_size?: number; q?: string } = {},
): Promise<PaginacionRespuesta<ProductoDTO>> {
  return requestJson<PaginacionRespuesta<ProductoDTO>>(
    `${API_BASE}/productos${toQuery(params)}`,
    { method: 'GET', headers: authHeaders(token) },
  )
}

export async function crearProducto(token: string, payload: CrearProductoDTO): Promise<ProductoDTO> {
  return requestJson<ProductoDTO>(`${API_BASE}/productos`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
}

export async function eliminarProducto(token: string, productoId: number): Promise<{ status: string }> {
  return requestJson<{ status: string }>(`${API_BASE}/productos/${productoId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  })
}

export async function listarBodegas(
  token: string,
  params: { page?: number; page_size?: number; q?: string; pais?: string } = {},
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
  params: { page?: number; page_size?: number; q?: string; pais?: string } = {},
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

export async function listarEnvios(
  token: string,
  params: {
    page?: number
    page_size?: number
    q?: string
    cliente_id?: number
    producto_id?: number
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
