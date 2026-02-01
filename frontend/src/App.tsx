import { useMemo, useState, type SubmitEvent } from 'react'
import './App.css'

import {
  cotizarMaritimo,
  cotizarTerrestre,
  login,
  type CotizacionMaritimaRequest,
  type CotizacionTerrestreRequest,
} from './api'
import { guardarToken, leerToken, limpiarToken } from './almacen_token'

function App() {
  const [token, setToken] = useState<string>(() => leerToken())
  const [mensaje, setMensaje] = useState<string>('')
  const [cargando, setCargando] = useState<boolean>(false)

  const [usuario, setUsuario] = useState('admin')
  const [contrasena, setContrasena] = useState('admin')

  const [modo, setModo] = useState<'terrestre' | 'maritimo'>('terrestre')

  const [formTerrestre, setFormTerrestre] = useState<CotizacionTerrestreRequest>({
    guia: 'GUIA-2026-000001',
    cliente_id: 1,
    placa_vehiculo: 'ABC123',
    codigo_flota: 'FLT-0001',
    cantidad: 10,
  })

  const [formMaritimo, setFormMaritimo] = useState<CotizacionMaritimaRequest>({
    guia: 'GUIA-2026-000002',
    cliente_id: 1,
    puerto_origen_id: 1,
    puerto_destino_id: 2,
    cantidad: 50,
  })

  const autorizado = useMemo(() => token.trim().length > 0, [token])

  const onLogin = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await login(usuario, contrasena)
        guardarToken(resp.access_token)
        setToken(resp.access_token)
        setMensaje('Login OK. Token guardado.')
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error de login')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onCotizar = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        if (!autorizado) throw new Error('Primero inicia sesión (token Bearer).')

        const resp =
          modo === 'terrestre'
            ? await cotizarTerrestre(token, formTerrestre)
            : await cotizarMaritimo(token, formMaritimo)

        setMensaje(`Cotización OK:\n${JSON.stringify(resp, null, 2)}`)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error al cotizar')
      } finally {
        setCargando(false)
      }
    })()
  }

  function onLogout() {
    limpiarToken()
    setToken('')
    setMensaje('Sesión cerrada.')
  }

  return (
    <>
      <h1>Plataforma Logística</h1>
      <p className="read-the-docs">
        Frontend (React + Vite) consumiendo la API vía proxy <code>/api</code>
      </p>

      <div className="card" style={{ textAlign: 'left' }}>
        <h2>Autenticación</h2>

        <form onSubmit={onLogin} style={{ display: 'grid', gap: 8, maxWidth: 420 }}>
          <label>
            <span>Usuario</span>
            <input
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              placeholder="admin"
              autoComplete="username"
            />
          </label>

          <label>
            <span>Contraseña</span>
            <input
              value={contrasena}
              onChange={(e) => setContrasena(e.target.value)}
              placeholder="admin"
              type="password"
              autoComplete="current-password"
            />
          </label>

          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <button type="submit" disabled={cargando}>
              {cargando ? 'Cargando...' : 'Iniciar sesión'}
            </button>
            <button type="button" onClick={onLogout} disabled={!autorizado || cargando}>
              Cerrar sesión
            </button>
          </div>

          <small>
            Token: {autorizado ? `${token.slice(0, 18)}...` : '(sin token)'}
          </small>
        </form>
      </div>

      <div className="card" style={{ textAlign: 'left' }}>
        <h2>Cotización de envíos</h2>

        <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 8 }}>
          <label>
            <span>Tipo</span>
            <select value={modo} onChange={(e) => setModo(e.target.value as any)}>
              <option value="terrestre">Terrestre</option>
              <option value="maritimo">Marítimo</option>
            </select>
          </label>
          <small>
            <span>Endpoints: </span>
            <code>/api/v1/envios/terrestres/cotizar</code>
            <span> / </span>
            <code>/api/v1/envios/maritimos/cotizar</code>
          </small>
        </div>

        <form onSubmit={onCotizar} style={{ display: 'grid', gap: 8, maxWidth: 520 }}>
          {modo === 'terrestre' ? (
            <>
              <label>
                <span>Guía</span>
                <input
                  value={formTerrestre.guia}
                  onChange={(e) => setFormTerrestre({ ...formTerrestre, guia: e.target.value })}
                />
              </label>
              <label>
                <span>Cliente ID</span>
                <input
                  type="number"
                  value={formTerrestre.cliente_id}
                  onChange={(e) =>
                    setFormTerrestre({ ...formTerrestre, cliente_id: Number(e.target.value) })
                  }
                />
              </label>
              <label>
                <span>Placa vehículo</span>
                <input
                  value={formTerrestre.placa_vehiculo}
                  onChange={(e) =>
                    setFormTerrestre({ ...formTerrestre, placa_vehiculo: e.target.value })
                  }
                />
              </label>
              <label>
                <span>Código flota</span>
                <input
                  value={formTerrestre.codigo_flota}
                  onChange={(e) =>
                    setFormTerrestre({ ...formTerrestre, codigo_flota: e.target.value })
                  }
                />
              </label>
              <label>
                <span>Cantidad</span>
                <input
                  type="number"
                  value={formTerrestre.cantidad}
                  onChange={(e) =>
                    setFormTerrestre({ ...formTerrestre, cantidad: Number(e.target.value) })
                  }
                />
              </label>
            </>
          ) : (
            <>
              <label>
                <span>Guía</span>
                <input
                  value={formMaritimo.guia}
                  onChange={(e) => setFormMaritimo({ ...formMaritimo, guia: e.target.value })}
                />
              </label>
              <label>
                <span>Cliente ID</span>
                <input
                  type="number"
                  value={formMaritimo.cliente_id}
                  onChange={(e) =>
                    setFormMaritimo({ ...formMaritimo, cliente_id: Number(e.target.value) })
                  }
                />
              </label>
              <label>
                <span>Puerto origen ID</span>
                <input
                  type="number"
                  value={formMaritimo.puerto_origen_id}
                  onChange={(e) =>
                    setFormMaritimo({ ...formMaritimo, puerto_origen_id: Number(e.target.value) })
                  }
                />
              </label>
              <label>
                <span>Puerto destino ID</span>
                <input
                  type="number"
                  value={formMaritimo.puerto_destino_id}
                  onChange={(e) =>
                    setFormMaritimo({ ...formMaritimo, puerto_destino_id: Number(e.target.value) })
                  }
                />
              </label>
              <label>
                <span>Cantidad</span>
                <input
                  type="number"
                  value={formMaritimo.cantidad}
                  onChange={(e) =>
                    setFormMaritimo({ ...formMaritimo, cantidad: Number(e.target.value) })
                  }
                />
              </label>
            </>
          )}

          <button type="submit" disabled={cargando}>
            {cargando ? 'Cotizando...' : 'Cotizar'}
          </button>
        </form>
      </div>

      {mensaje ? (
        <pre className="card" style={{ textAlign: 'left', whiteSpace: 'pre-wrap' }}>
          {mensaje}
        </pre>
      ) : null}
    </>
  )
}

export default App
