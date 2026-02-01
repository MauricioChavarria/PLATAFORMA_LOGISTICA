const KEY = 'token_bearer'

export function guardarToken(token: string): void {
  localStorage.setItem(KEY, token)
}

export function leerToken(): string {
  return localStorage.getItem(KEY) ?? ''
}

export function limpiarToken(): void {
  localStorage.removeItem(KEY)
}
