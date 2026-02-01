import { useMemo, useState, type SubmitEvent } from 'react'
import './App.css'

import {
  cotizarMaritimo,
  cotizarTerrestre,
  crearCliente,
  crearBodega,
  crearEnvio,
  crearProducto,
  crearPuerto,
  eliminarCliente,
  eliminarBodega,
  eliminarEnvio,
  eliminarProducto,
  eliminarPuerto,
  listarClientes,
  listarBodegas,
  listarEnvios,
  listarProductos,
  listarPuertos,
  login,
  type ClienteDTO,
  type CrearClienteDTO,
  type CrearBodegaDTO,
  type CrearEnvioDTO,
  type CrearProductoDTO,
  type CrearPuertoDTO,
  type CotizacionMaritimaRequest,
  type CotizacionTerrestreRequest,
  type EnvioDTO,
  type ProductoDTO,
  type BodegaDTO,
  type PuertoDTO,
  type TipoEnvio,
} from './api'
import { guardarToken, leerToken, limpiarToken } from './almacen_token'

type Vista = 'cotizar' | 'clientes' | 'productos' | 'bodegas' | 'puertos' | 'envios'

function App() {
  const [token, setToken] = useState<string>(() => leerToken())
  const [mensaje, setMensaje] = useState<string>('')
  const [cargando, setCargando] = useState<boolean>(false)

  const [vista, setVista] = useState<Vista>('cotizar')

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
    setVista('cotizar')
  }

  return (
    <>
      <h1>Plataforma Logística</h1>
      <p className="read-the-docs">
        Frontend (React + Vite) consumiendo la API vía proxy <code>/api</code>
      </p>

      <div className="card" style={{ textAlign: 'left' }}>
        <h2>Navegación</h2>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center' }}>
          <button type="button" onClick={() => setVista('cotizar')} disabled={cargando}>
            Cotizar
          </button>
          <button type="button" onClick={() => setVista('clientes')} disabled={cargando || !autorizado}>
            Clientes
          </button>
          <button type="button" onClick={() => setVista('productos')} disabled={cargando || !autorizado}>
            Productos
          </button>
          <button type="button" onClick={() => setVista('bodegas')} disabled={cargando || !autorizado}>
            Bodegas
          </button>
          <button type="button" onClick={() => setVista('puertos')} disabled={cargando || !autorizado}>
            Puertos
          </button>
          <button type="button" onClick={() => setVista('envios')} disabled={cargando || !autorizado}>
            Envíos
          </button>
          {autorizado ? null : <small>Inicia sesión para CRUD.</small>}
        </div>
      </div>

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

      {vista === 'productos' ? (
        <ProductosPanel token={token} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'clientes' ? (
        <ClientesPanel token={token} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'bodegas' ? (
        <BodegasPanel token={token} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'puertos' ? (
        <PuertosPanel token={token} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'envios' ? (
        <EnviosPanel token={token} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {mensaje ? (
        <pre className="card" style={{ textAlign: 'left', whiteSpace: 'pre-wrap' }}>
          {mensaje}
        </pre>
      ) : null}
    </>
  )
}

export default App

function ClientesPanel(
  props: Readonly<{
    token: string
    setMensaje: (s: string) => void
    setCargando: (b: boolean) => void
  }>,
) {
  const { token, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [email, setEmail] = useState<string>('')
  const [documento, setDocumento] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<ClienteDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearClienteDTO>({
    nombre: '',
    email: '',
    documento: '',
    telefono: '',
  })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarClientes(token, {
          page,
          page_size: pageSize,
          q: q.trim() || undefined,
          email: email.trim() || undefined,
          documento: documento.trim() || undefined,
        })
        setItems(resp.items)
        setTotal(resp.total)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error cargando clientes')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onCrear = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await crearCliente(token, {
          nombre: nuevo.nombre,
          email: nuevo.email,
          documento: nuevo.documento,
          telefono: nuevo.telefono?.trim() ? nuevo.telefono : null,
        })
        setNuevo({ nombre: '', email: '', documento: '', telefono: '' })
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error creando cliente')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onEliminar = (id: number) => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await eliminarCliente(token, id)
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error eliminando cliente')
      } finally {
        setCargando(false)
      }
    })()
  }

  return (
    <div className="card" style={{ textAlign: 'left' }}>
      <h2>Clientes</h2>

      <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 640, marginBottom: 12 }}>
        <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
          <label>
            <span>Nombre</span>
            <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
          </label>
          <label>
            <span>Email</span>
            <input value={nuevo.email} onChange={(e) => setNuevo({ ...nuevo, email: e.target.value })} />
          </label>
          <label>
            <span>Documento</span>
            <input
              value={nuevo.documento}
              onChange={(e) => setNuevo({ ...nuevo, documento: e.target.value })}
            />
          </label>
          <label>
            <span>Teléfono</span>
            <input value={nuevo.telefono ?? ''} onChange={(e) => setNuevo({ ...nuevo, telefono: e.target.value })} />
          </label>
        </div>

        <button type="submit">Crear cliente</button>
      </form>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>
          <span>Buscar</span>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="q (nombre/email/doc)" />
        </label>
        <label>
          <span>Email</span>
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="" />
        </label>
        <label>
          <span>Documento</span>
          <input value={documento} onChange={(e) => setDocumento(e.target.value)} placeholder="" />
        </label>
        <label>
          <span>Page</span>
          <input type="number" value={page} min={1} onChange={(e) => setPage(Number(e.target.value))} />
        </label>
        <label>
          <span>Page size</span>
          <input
            type="number"
            value={pageSize}
            min={1}
            max={100}
            onChange={(e) => setPageSize(Number(e.target.value))}
          />
        </label>
        <button type="button" onClick={cargar}>
          Refrescar
        </button>
        <small>Total: {total}</small>
      </div>

      <div style={{ marginTop: 12 }}>
        {items.length === 0 ? (
          <small>Sin resultados.</small>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>ID</th>
                <th style={{ textAlign: 'left' }}>Nombre</th>
                <th style={{ textAlign: 'left' }}>Email</th>
                <th style={{ textAlign: 'left' }}>Documento</th>
                <th style={{ textAlign: 'left' }}>Teléfono</th>
                <th style={{ textAlign: 'left' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.map((c) => (
                <tr key={c.id}>
                  <td>{c.id}</td>
                  <td>{c.nombre}</td>
                  <td>{c.email}</td>
                  <td>{c.documento}</td>
                  <td>{c.telefono ?? ''}</td>
                  <td>
                    <button type="button" onClick={() => onEliminar(c.id)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

function ProductosPanel(
  props: Readonly<{
  token: string
  setMensaje: (s: string) => void
  setCargando: (b: boolean) => void
  }>,
) {
  const { token, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<ProductoDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearProductoDTO>({ nombre: '', descripcion: '' })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarProductos(token, { page, page_size: pageSize, q: q.trim() || undefined })
        setItems(resp.items)
        setTotal(resp.total)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error cargando productos')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onCrear = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await crearProducto(token, { nombre: nuevo.nombre, descripcion: nuevo.descripcion || null })
        setNuevo({ nombre: '', descripcion: '' })
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error creando producto')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onEliminar = (id: number) => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await eliminarProducto(token, id)
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error eliminando producto')
      } finally {
        setCargando(false)
      }
    })()
  }

  return (
    <div className="card" style={{ textAlign: 'left' }}>
      <h2>Productos</h2>

      <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 520, marginBottom: 12 }}>
        <label>
          <span>Nombre</span>
          <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
        </label>
        <label>
          <span>Descripción</span>
          <input
            value={nuevo.descripcion ?? ''}
            onChange={(e) => setNuevo({ ...nuevo, descripcion: e.target.value })}
          />
        </label>
        <button type="submit">Crear producto</button>
      </form>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>
          <span>Buscar</span>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="q (nombre)" />
        </label>
        <label>
          <span>Page</span>
          <input type="number" value={page} min={1} onChange={(e) => setPage(Number(e.target.value))} />
        </label>
        <label>
          <span>Page size</span>
          <input
            type="number"
            value={pageSize}
            min={1}
            max={100}
            onChange={(e) => setPageSize(Number(e.target.value))}
          />
        </label>
        <button type="button" onClick={cargar}>
          Refrescar
        </button>
        <small>Total: {total}</small>
      </div>

      <div style={{ marginTop: 12 }}>
        {items.length === 0 ? (
          <small>Sin resultados.</small>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>ID</th>
                <th style={{ textAlign: 'left' }}>Nombre</th>
                <th style={{ textAlign: 'left' }}>Descripción</th>
                <th style={{ textAlign: 'left' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.nombre}</td>
                  <td>{p.descripcion ?? ''}</td>
                  <td>
                    <button type="button" onClick={() => onEliminar(p.id)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

function BodegasPanel(
  props: Readonly<{
  token: string
  setMensaje: (s: string) => void
  setCargando: (b: boolean) => void
  }>,
) {
  const { token, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [pais, setPais] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<BodegaDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearBodegaDTO>({ nombre: '', ubicacion: '', pais: '' })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarBodegas(token, {
          page,
          page_size: pageSize,
          q: q.trim() || undefined,
          pais: pais.trim() || undefined,
        })
        setItems(resp.items)
        setTotal(resp.total)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error cargando bodegas')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onCrear = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await crearBodega(token, nuevo)
        setNuevo({ nombre: '', ubicacion: '', pais: '' })
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error creando bodega')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onEliminar = (id: number) => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await eliminarBodega(token, id)
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error eliminando bodega')
      } finally {
        setCargando(false)
      }
    })()
  }

  return (
    <div className="card" style={{ textAlign: 'left' }}>
      <h2>Bodegas</h2>

      <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 520, marginBottom: 12 }}>
        <label>
          <span>Nombre</span>
          <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
        </label>
        <label>
          <span>Ubicación</span>
          <input
            value={nuevo.ubicacion}
            onChange={(e) => setNuevo({ ...nuevo, ubicacion: e.target.value })}
          />
        </label>
        <label>
          <span>País</span>
          <input value={nuevo.pais} onChange={(e) => setNuevo({ ...nuevo, pais: e.target.value })} />
        </label>
        <button type="submit">Crear bodega</button>
      </form>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>
          <span>Buscar</span>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="q (nombre)" />
        </label>
        <label>
          <span>País</span>
          <input value={pais} onChange={(e) => setPais(e.target.value)} placeholder="CO" />
        </label>
        <label>
          <span>Page</span>
          <input type="number" value={page} min={1} onChange={(e) => setPage(Number(e.target.value))} />
        </label>
        <label>
          <span>Page size</span>
          <input
            type="number"
            value={pageSize}
            min={1}
            max={100}
            onChange={(e) => setPageSize(Number(e.target.value))}
          />
        </label>
        <button type="button" onClick={cargar}>
          Refrescar
        </button>
        <small>Total: {total}</small>
      </div>

      <div style={{ marginTop: 12 }}>
        {items.length === 0 ? (
          <small>Sin resultados.</small>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>ID</th>
                <th style={{ textAlign: 'left' }}>Nombre</th>
                <th style={{ textAlign: 'left' }}>Ubicación</th>
                <th style={{ textAlign: 'left' }}>País</th>
                <th style={{ textAlign: 'left' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.map((b) => (
                <tr key={b.id}>
                  <td>{b.id}</td>
                  <td>{b.nombre}</td>
                  <td>{b.ubicacion}</td>
                  <td>{b.pais}</td>
                  <td>
                    <button type="button" onClick={() => onEliminar(b.id)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

function PuertosPanel(
  props: Readonly<{
  token: string
  setMensaje: (s: string) => void
  setCargando: (b: boolean) => void
  }>,
) {
  const { token, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [pais, setPais] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<PuertoDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearPuertoDTO>({ nombre: '', pais: '' })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarPuertos(token, {
          page,
          page_size: pageSize,
          q: q.trim() || undefined,
          pais: pais.trim() || undefined,
        })
        setItems(resp.items)
        setTotal(resp.total)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error cargando puertos')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onCrear = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await crearPuerto(token, nuevo)
        setNuevo({ nombre: '', pais: '' })
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error creando puerto')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onEliminar = (id: number) => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await eliminarPuerto(token, id)
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error eliminando puerto')
      } finally {
        setCargando(false)
      }
    })()
  }

  return (
    <div className="card" style={{ textAlign: 'left' }}>
      <h2>Puertos</h2>

      <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 520, marginBottom: 12 }}>
        <label>
          <span>Nombre</span>
          <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
        </label>
        <label>
          <span>País</span>
          <input value={nuevo.pais} onChange={(e) => setNuevo({ ...nuevo, pais: e.target.value })} />
        </label>
        <button type="submit">Crear puerto</button>
      </form>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>
          <span>Buscar</span>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="q (nombre)" />
        </label>
        <label>
          <span>País</span>
          <input value={pais} onChange={(e) => setPais(e.target.value)} placeholder="CO" />
        </label>
        <label>
          <span>Page</span>
          <input type="number" value={page} min={1} onChange={(e) => setPage(Number(e.target.value))} />
        </label>
        <label>
          <span>Page size</span>
          <input
            type="number"
            value={pageSize}
            min={1}
            max={100}
            onChange={(e) => setPageSize(Number(e.target.value))}
          />
        </label>
        <button type="button" onClick={cargar}>
          Refrescar
        </button>
        <small>Total: {total}</small>
      </div>

      <div style={{ marginTop: 12 }}>
        {items.length === 0 ? (
          <small>Sin resultados.</small>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>ID</th>
                <th style={{ textAlign: 'left' }}>Nombre</th>
                <th style={{ textAlign: 'left' }}>País</th>
                <th style={{ textAlign: 'left' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.nombre}</td>
                  <td>{p.pais}</td>
                  <td>
                    <button type="button" onClick={() => onEliminar(p.id)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

function EnviosPanel(
  props: Readonly<{
  token: string
  setMensaje: (s: string) => void
  setCargando: (b: boolean) => void
  }>,
) {
  const { token, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [tipo, setTipo] = useState<TipoEnvio | ''>('')
  const [clienteId, setClienteId] = useState<string>('')
  const [productoId, setProductoId] = useState<string>('')

  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<EnvioDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const hoy = new Date().toISOString().slice(0, 10)
  const [nuevo, setNuevo] = useState<CrearEnvioDTO>({
    cliente_id: 1,
    producto_id: 1,
    cantidad: 1,
    fecha_registro: hoy,
    fecha_entrega: hoy,
    precio_base: '0',
    descuento: '0',
    numero_guia: 'GUIA-0001',
    tipo_envio: 'TERRESTRE',
    bodega_id: 1,
    placa_vehiculo: 'ABC123',
  })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarEnvios(token, {
          page,
          page_size: pageSize,
          q: q.trim() || undefined,
          tipo_envio: tipo || undefined,
          cliente_id: clienteId.trim() ? Number(clienteId) : undefined,
          producto_id: productoId.trim() ? Number(productoId) : undefined,
        })
        setItems(resp.items)
        setTotal(resp.total)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error cargando envíos')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onCrear = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const payload: CrearEnvioDTO = {
          ...nuevo,
          cliente_id: Number(nuevo.cliente_id),
          producto_id: Number(nuevo.producto_id),
          cantidad: Number(nuevo.cantidad),
        }

        if (payload.tipo_envio === 'TERRESTRE') {
          delete (payload as any).puerto_id
          delete (payload as any).numero_flota
        }
        if (payload.tipo_envio === 'MARITIMO') {
          delete (payload as any).bodega_id
          delete (payload as any).placa_vehiculo
        }

        await crearEnvio(token, payload)
        setMensaje('Envío creado.')
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error creando envío')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onEliminar = (id: number) => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        await eliminarEnvio(token, id)
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error eliminando envío')
      } finally {
        setCargando(false)
      }
    })()
  }

  return (
    <div className="card" style={{ textAlign: 'left' }}>
      <h2>Envíos</h2>

      <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 720, marginBottom: 12 }}>
        <label>
          <span>Tipo envío</span>
          <select
            value={nuevo.tipo_envio}
            onChange={(e) => {
              const t = e.target.value as TipoEnvio
              if (t === 'TERRESTRE') {
                setNuevo({ ...nuevo, tipo_envio: t, bodega_id: nuevo.bodega_id ?? 1, placa_vehiculo: nuevo.placa_vehiculo ?? '' })
              } else {
                setNuevo({
                  ...nuevo,
                  tipo_envio: t,
                  puerto_id: (nuevo as any).puerto_id ?? 1,
                  numero_flota: (nuevo as any).numero_flota ?? 'F-01',
                })
              }
            }}
          >
            <option value="TERRESTRE">TERRESTRE</option>
            <option value="MARITIMO">MARITIMO</option>
          </select>
        </label>

        <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
          <label>
            <span>Cliente ID</span>
            <input
              type="number"
              value={nuevo.cliente_id}
              onChange={(e) => setNuevo({ ...nuevo, cliente_id: Number(e.target.value) })}
            />
          </label>
          <label>
            <span>Producto ID</span>
            <input
              type="number"
              value={nuevo.producto_id}
              onChange={(e) => setNuevo({ ...nuevo, producto_id: Number(e.target.value) })}
            />
          </label>
          <label>
            <span>Cantidad</span>
            <input
              type="number"
              value={nuevo.cantidad}
              onChange={(e) => setNuevo({ ...nuevo, cantidad: Number(e.target.value) })}
            />
          </label>
          <label>
            <span>Número guía</span>
            <input value={nuevo.numero_guia} onChange={(e) => setNuevo({ ...nuevo, numero_guia: e.target.value })} />
          </label>
          <label>
            <span>Fecha registro</span>
            <input
              type="date"
              value={nuevo.fecha_registro}
              onChange={(e) => setNuevo({ ...nuevo, fecha_registro: e.target.value })}
            />
          </label>
          <label>
            <span>Fecha entrega</span>
            <input
              type="date"
              value={nuevo.fecha_entrega}
              onChange={(e) => setNuevo({ ...nuevo, fecha_entrega: e.target.value })}
            />
          </label>
          <label>
            <span>Precio base</span>
            <input
              value={String(nuevo.precio_base)}
              onChange={(e) => setNuevo({ ...nuevo, precio_base: e.target.value })}
            />
          </label>
          <label>
            <span>Descuento</span>
            <input
              value={String(nuevo.descuento)}
              onChange={(e) => setNuevo({ ...nuevo, descuento: e.target.value })}
            />
          </label>
        </div>

        {nuevo.tipo_envio === 'TERRESTRE' ? (
          <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
            <label>
              <span>Bodega ID</span>
              <input
                type="number"
                value={nuevo.bodega_id ?? 1}
                onChange={(e) => setNuevo({ ...nuevo, bodega_id: Number(e.target.value) })}
              />
            </label>
            <label>
              <span>Placa vehículo</span>
              <input
                value={nuevo.placa_vehiculo ?? ''}
                onChange={(e) => setNuevo({ ...nuevo, placa_vehiculo: e.target.value })}
              />
            </label>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
            <label>
              <span>Puerto ID</span>
              <input
                type="number"
                value={(nuevo as any).puerto_id ?? 1}
                onChange={(e) => setNuevo({ ...nuevo, puerto_id: Number(e.target.value) })}
              />
            </label>
            <label>
              <span>Número flota</span>
              <input
                value={(nuevo as any).numero_flota ?? ''}
                onChange={(e) => setNuevo({ ...nuevo, numero_flota: e.target.value })}
              />
            </label>
          </div>
        )}

        <button type="submit">Crear envío</button>
      </form>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>
          <span>Buscar guía</span>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="q (numero_guia)" />
        </label>
        <label>
          <span>Tipo</span>
          <select value={tipo} onChange={(e) => setTipo(e.target.value as any)}>
            <option value="">(todos)</option>
            <option value="TERRESTRE">TERRESTRE</option>
            <option value="MARITIMO">MARITIMO</option>
          </select>
        </label>
        <label>
          <span>Cliente ID</span>
          <input value={clienteId} onChange={(e) => setClienteId(e.target.value)} placeholder="" />
        </label>
        <label>
          <span>Producto ID</span>
          <input value={productoId} onChange={(e) => setProductoId(e.target.value)} placeholder="" />
        </label>
        <label>
          <span>Page</span>
          <input type="number" value={page} min={1} onChange={(e) => setPage(Number(e.target.value))} />
        </label>
        <label>
          <span>Page size</span>
          <input
            type="number"
            value={pageSize}
            min={1}
            max={100}
            onChange={(e) => setPageSize(Number(e.target.value))}
          />
        </label>
        <button type="button" onClick={cargar}>
          Refrescar
        </button>
        <small>Total: {total}</small>
      </div>

      <div style={{ marginTop: 12 }}>
        {items.length === 0 ? (
          <small>Sin resultados.</small>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>ID</th>
                <th style={{ textAlign: 'left' }}>Guía</th>
                <th style={{ textAlign: 'left' }}>Tipo</th>
                <th style={{ textAlign: 'left' }}>Cliente</th>
                <th style={{ textAlign: 'left' }}>Producto</th>
                <th style={{ textAlign: 'left' }}>Final</th>
                <th style={{ textAlign: 'left' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.map((e) => (
                <tr key={e.id}>
                  <td>{e.id}</td>
                  <td>{e.numero_guia}</td>
                  <td>{e.tipo_envio}</td>
                  <td>{e.cliente_id}</td>
                  <td>{e.producto_id}</td>
                  <td>{e.precio_final}</td>
                  <td>
                    <button type="button" onClick={() => onEliminar(e.id)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
