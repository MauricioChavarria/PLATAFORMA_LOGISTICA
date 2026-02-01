export type TokenResponse = {
  access_token: string
  token_type: 'bearer'
}

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
