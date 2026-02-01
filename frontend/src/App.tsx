import { useEffect, useMemo, useState, type SubmitEvent } from 'react'
import './App.css'

import {
  crearBodega,
  crearCliente,
  crearEnvio,
  crearPuerto,
  crearTipoProducto,
  eliminarBodega,
  eliminarCliente,
  eliminarEnvio,
  eliminarPuerto,
  eliminarTipoProducto,
  listarBodegas,
  listarClientes,
  listarEnvios,
  listarPuertos,
  listarTiposProducto,
  login,
  me,
  register,
  type CrearBodegaDTO,
  type CrearClienteDTO,
  type CrearEnvioDTO,
  type CrearPuertoDTO,
  type CrearTipoProductoDTO,
  type EnvioDTO,
  type BodegaDTO,
  type ClienteDTO,
  type MeResponse,
  type PuertoDTO,
  type TipoEnvio,
  type TipoProductoDTO,
} from './api'
import { guardarToken, leerToken, limpiarToken } from './almacen_token'

type Vista = 'clientes' | 'tipos_producto' | 'bodegas' | 'puertos' | 'envios'

function App() {
  const [token, setToken] = useState<string>(() => leerToken())
  const [mensaje, setMensaje] = useState<string>('')
  const [cargando, setCargando] = useState<boolean>(false)

  const [meInfo, setMeInfo] = useState<MeResponse | null>(null)

  const [vista, setVista] = useState<Vista>('tipos_producto')

  const [modoAuth, setModoAuth] = useState<'login' | 'register'>('login')
  const [usuario, setUsuario] = useState('admin')
  const [contrasena, setContrasena] = useState('admin')
  const [contrasena2, setContrasena2] = useState('')

  const autorizado = useMemo(() => token.trim().length > 0, [token])
  const esAdmin = useMemo(() => meInfo?.role === 'admin', [meInfo])
  const submitLabel = useMemo(() => (modoAuth === 'login' ? 'Iniciar sesión' : 'Crear cuenta'), [modoAuth])

  useEffect(() => {
    if (!token.trim()) {
      setMeInfo(null)
      return
    }

    void (async () => {
      try {
        const info = await me(token)
        setMeInfo(info)
      } catch (err: any) {
        // token inválido/expirado
        limpiarToken()
        setToken('')
        setMeInfo(null)
        setMensaje(err?.message ?? 'Token inválido. Vuelve a iniciar sesión.')
      }
    })()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token])

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

  const onRegister = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      setMensaje('')

      if (usuario.trim().toLowerCase() === 'admin') {
        setMensaje('El usuario "admin" está reservado (demo). Usa otro username.')
        return
      }
      if (!usuario.trim()) {
        setMensaje('Username requerido')
        return
      }
      if (!contrasena.trim()) {
        setMensaje('Contraseña requerida')
        return
      }
      if (contrasena !== contrasena2) {
        setMensaje('Las contraseñas no coinciden')
        return
      }

      setCargando(true)
      try {
        await register({ username: usuario.trim(), password: contrasena })
        const resp = await login(usuario, contrasena)
        guardarToken(resp.access_token)
        setToken(resp.access_token)
        setMensaje('Registro OK. Sesión iniciada.')
        setModoAuth('login')
        setContrasena2('')
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error registrando usuario')
      } finally {
        setCargando(false)
      }
    })()
  }

  function onLogout() {
    limpiarToken()
    setToken('')
    setMeInfo(null)
    setMensaje('Sesión cerrada.')
    setVista('tipos_producto')
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
          <button type="button" onClick={() => setVista('clientes')} disabled={cargando || !autorizado}>
            Clientes
          </button>
          <button type="button" onClick={() => setVista('tipos_producto')} disabled={cargando || !autorizado}>
            Tipos de producto
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

        <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8 }}>
          <button
            type="button"
            onClick={() => setModoAuth('login')}
            disabled={cargando || modoAuth === 'login'}
          >
            Login
          </button>
          <button
            type="button"
            onClick={() => setModoAuth('register')}
            disabled={cargando || modoAuth === 'register'}
          >
            Registro
          </button>
        </div>

        <form
          onSubmit={modoAuth === 'login' ? onLogin : onRegister}
          style={{ display: 'grid', gap: 8, maxWidth: 420 }}
        >
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
              autoComplete={modoAuth === 'login' ? 'current-password' : 'new-password'}
            />
          </label>

          {modoAuth === 'register' ? (
            <label>
              <span>Confirmar contraseña</span>
              <input
                value={contrasena2}
                onChange={(e) => setContrasena2(e.target.value)}
                type="password"
                autoComplete="new-password"
              />
            </label>
          ) : null}

          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <button type="submit" disabled={cargando}>
              {cargando ? 'Cargando...' : submitLabel}
            </button>
            <button type="button" onClick={onLogout} disabled={!autorizado || cargando}>
              Cerrar sesión
            </button>
          </div>

          <small>
            Token: {autorizado ? `${token.slice(0, 18)}...` : '(sin token)'}
          </small>
          <small>
            Usuario actual: {meInfo ? `${meInfo.sub} (${meInfo.role})` : '(desconocido)'}
          </small>
        </form>
      </div>

      {vista === 'tipos_producto' ? (
        <TiposProductoPanel token={token} esAdmin={esAdmin} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'clientes' ? (
        <ClientesPanel token={token} esAdmin={esAdmin} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'bodegas' ? (
        <BodegasPanel token={token} esAdmin={esAdmin} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'puertos' ? (
        <PuertosPanel token={token} esAdmin={esAdmin} setMensaje={setMensaje} setCargando={setCargando} />
      ) : null}

      {vista === 'envios' ? (
        <EnviosPanel token={token} esAdmin={esAdmin} setMensaje={setMensaje} setCargando={setCargando} />
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

function TiposProductoPanel(
  props: Readonly<{
    token: string
    esAdmin: boolean
    setMensaje: (s: string) => void
    setCargando: (b: boolean) => void
  }>,
) {
  const { token, esAdmin, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<TipoProductoDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearTipoProductoDTO>({ nombre: '' })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarTiposProducto(token, { page, page_size: pageSize, q: q.trim() || undefined })
        setItems(resp.items)
        setTotal(resp.total)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error cargando tipos de producto')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onCrear = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    void (async () => {
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
      setMensaje('')
      setCargando(true)
      try {
        await crearTipoProducto(token, { nombre: nuevo.nombre })
        setNuevo({ nombre: '' })
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error creando tipo de producto')
      } finally {
        setCargando(false)
      }
    })()
  }

  const onEliminar = (id: number) => {
    void (async () => {
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
      setMensaje('')
      setCargando(true)
      try {
        await eliminarTipoProducto(token, id)
        cargar()
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error eliminando tipo de producto')
      } finally {
        setCargando(false)
      }
    })()
  }

  return (
    <div className="card" style={{ textAlign: 'left' }}>
      <h2>Tipos de producto</h2>

      {esAdmin ? (
        <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 520, marginBottom: 12 }}>
          <label>
            <span>Nombre</span>
            <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
          </label>
          <button type="submit">Crear tipo</button>
        </form>
      ) : (
        <small>Solo admin puede crear/eliminar tipos de producto.</small>
      )}

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
                {esAdmin ? <th style={{ textAlign: 'left' }}>Acciones</th> : null}
              </tr>
            </thead>
            <tbody>
              {items.map((t) => (
                <tr key={t.id_tipo_producto}>
                  <td>{t.id_tipo_producto}</td>
                  <td>{t.nombre}</td>
                  {esAdmin ? (
                    <td>
                      <button type="button" onClick={() => onEliminar(t.id_tipo_producto)}>
                        Eliminar
                      </button>
                    </td>
                  ) : null}
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
    esAdmin: boolean
    setMensaje: (s: string) => void
    setCargando: (b: boolean) => void
  }>,
) {
  const { token, esAdmin, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<BodegaDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearBodegaDTO>({ nombre: '', direccion: '' })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarBodegas(token, {
          page,
          page_size: pageSize,
          q: q.trim() || undefined,
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
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
      setMensaje('')
      setCargando(true)
      try {
        await crearBodega(token, { nombre: nuevo.nombre, direccion: nuevo.direccion?.trim() ? nuevo.direccion : null })
        setNuevo({ nombre: '', direccion: '' })
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
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
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

      {esAdmin ? (
        <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 520, marginBottom: 12 }}>
          <label>
            <span>Nombre</span>
            <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
          </label>
          <label>
            <span>Dirección</span>
            <input
              value={nuevo.direccion ?? ''}
              onChange={(e) => setNuevo({ ...nuevo, direccion: e.target.value })}
            />
          </label>
          <button type="submit">Crear bodega</button>
        </form>
      ) : (
        <small>Solo admin puede crear/eliminar bodegas.</small>
      )}

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
                <th style={{ textAlign: 'left' }}>Dirección</th>
                {esAdmin ? <th style={{ textAlign: 'left' }}>Acciones</th> : null}
              </tr>
            </thead>
            <tbody>
              {items.map((b) => (
                <tr key={b.id_bodega}>
                  <td>{b.id_bodega}</td>
                  <td>{b.nombre}</td>
                  <td>{b.direccion ?? ''}</td>
                  {esAdmin ? (
                    <td>
                      <button type="button" onClick={() => onEliminar(b.id_bodega)}>
                        Eliminar
                      </button>
                    </td>
                  ) : null}
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
    esAdmin: boolean
    setMensaje: (s: string) => void
    setCargando: (b: boolean) => void
  }>,
) {
  const { token, esAdmin, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [ciudad, setCiudad] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<PuertoDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearPuertoDTO>({ nombre: '', ciudad: '' })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarPuertos(token, {
          page,
          page_size: pageSize,
          q: q.trim() || undefined,
          ciudad: ciudad.trim() || undefined,
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
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
      setMensaje('')
      setCargando(true)
      try {
        await crearPuerto(token, { nombre: nuevo.nombre, ciudad: nuevo.ciudad?.trim() ? nuevo.ciudad : null })
        setNuevo({ nombre: '', ciudad: '' })
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
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
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

      {esAdmin ? (
        <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 520, marginBottom: 12 }}>
          <label>
            <span>Nombre</span>
            <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
          </label>
          <label>
            <span>Ciudad</span>
            <input value={nuevo.ciudad ?? ''} onChange={(e) => setNuevo({ ...nuevo, ciudad: e.target.value })} />
          </label>
          <button type="submit">Crear puerto</button>
        </form>
      ) : (
        <small>Solo admin puede crear/eliminar puertos.</small>
      )}

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>
          <span>Buscar</span>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="q (nombre)" />
        </label>
        <label>
          <span>Ciudad</span>
          <input value={ciudad} onChange={(e) => setCiudad(e.target.value)} placeholder="Cartagena" />
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
                <th style={{ textAlign: 'left' }}>Ciudad</th>
                {esAdmin ? <th style={{ textAlign: 'left' }}>Acciones</th> : null}
              </tr>
            </thead>
            <tbody>
              {items.map((p) => (
                <tr key={p.id_puerto}>
                  <td>{p.id_puerto}</td>
                  <td>{p.nombre}</td>
                  <td>{p.ciudad ?? ''}</td>
                  {esAdmin ? (
                    <td>
                      <button type="button" onClick={() => onEliminar(p.id_puerto)}>
                        Eliminar
                      </button>
                    </td>
                  ) : null}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

function ClientesPanel(
  props: Readonly<{
    token: string
    esAdmin: boolean
    setMensaje: (s: string) => void
    setCargando: (b: boolean) => void
  }>,
) {
  const { token, esAdmin, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<ClienteDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [nuevo, setNuevo] = useState<CrearClienteDTO>({ nombre: '', email: '', telefono: '' })

  const cargar = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const resp = await listarClientes(token, { page, page_size: pageSize, q: q.trim() || undefined })
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
          email: nuevo.email?.trim() ? nuevo.email.trim() : null,
          telefono: nuevo.telefono?.trim() ? nuevo.telefono.trim() : null,
        })
        setNuevo({ nombre: '', email: '', telefono: '' })
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
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
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

      <form onSubmit={onCrear} style={{ display: 'grid', gap: 8, maxWidth: 520, marginBottom: 12 }}>
        <label>
          <span>Nombre</span>
          <input value={nuevo.nombre} onChange={(e) => setNuevo({ ...nuevo, nombre: e.target.value })} />
        </label>
        <label>
          <span>Email</span>
          <input value={nuevo.email ?? ''} onChange={(e) => setNuevo({ ...nuevo, email: e.target.value })} />
        </label>
        <label>
          <span>Teléfono</span>
          <input value={nuevo.telefono ?? ''} onChange={(e) => setNuevo({ ...nuevo, telefono: e.target.value })} />
        </label>
        <button type="submit">Crear cliente</button>
      </form>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
        <label>
          <span>Buscar</span>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="q (nombre/email)" />
        </label>
        <label>
          <span>Page</span>
          <input type="number" value={page} min={1} onChange={(e) => setPage(Number(e.target.value))} />
        </label>
        <label>
          <span>Page size</span>
          <input type="number" value={pageSize} min={1} max={100} onChange={(e) => setPageSize(Number(e.target.value))} />
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
                <th style={{ textAlign: 'left' }}>Teléfono</th>
                {esAdmin ? <th style={{ textAlign: 'left' }}>Acciones</th> : null}
              </tr>
            </thead>
            <tbody>
              {items.map((c) => (
                <tr key={c.id_cliente}>
                  <td>{c.id_cliente}</td>
                  <td>{c.nombre}</td>
                  <td>{c.email ?? ''}</td>
                  <td>{c.telefono ?? ''}</td>
                  {esAdmin ? (
                    <td>
                      <button type="button" onClick={() => onEliminar(c.id_cliente)}>
                        Eliminar
                      </button>
                    </td>
                  ) : null}
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
    esAdmin: boolean
    setMensaje: (s: string) => void
    setCargando: (b: boolean) => void
  }>,
) {
  const { token, esAdmin, setMensaje, setCargando } = props

  const [q, setQ] = useState<string>('')
  const [tipo, setTipo] = useState<TipoEnvio | ''>('')
  const [clienteId, setClienteId] = useState<string>('')
  const [tipoProductoId, setTipoProductoId] = useState<string>('')

  const [page, setPage] = useState<number>(1)
  const [pageSize, setPageSize] = useState<number>(10)
  const [items, setItems] = useState<EnvioDTO[]>([])
  const [total, setTotal] = useState<number>(0)

  const [catalogoTiposProducto, setCatalogoTiposProducto] = useState<TipoProductoDTO[]>([])
  const [catalogoBodegas, setCatalogoBodegas] = useState<BodegaDTO[]>([])
  const [catalogoPuertos, setCatalogoPuertos] = useState<PuertoDTO[]>([])
  const [catalogoClientes, setCatalogoClientes] = useState<ClienteDTO[]>([])

  const hoy = new Date().toISOString().slice(0, 10)
  const [nuevo, setNuevo] = useState<CrearEnvioDTO>({
    id_cliente: 1,
    id_tipo_producto: 1,
    cantidad: 1,
    fecha_registro: hoy,
    fecha_entrega: hoy,
    precio_base: '0',
    numero_guia: 'GUIA0001',
    tipo_envio: 'TERRESTRE',
    id_bodega: 1,
    placa_vehiculo: 'ABC123',
    id_puerto: 1,
    numero_flota: 'ABC1234Z',
  })

  const cargarCatalogos = () => {
    void (async () => {
      setMensaje('')
      setCargando(true)
      try {
        const [clientesResp, tiposResp, bodegasResp, puertosResp] = await Promise.all([
          listarClientes(token, { page: 1, page_size: 100 }),
          listarTiposProducto(token, { page: 1, page_size: 100 }),
          listarBodegas(token, { page: 1, page_size: 100 }),
          listarPuertos(token, { page: 1, page_size: 100 }),
        ])
        setCatalogoClientes(clientesResp.items)
        setCatalogoTiposProducto(tiposResp.items)
        setCatalogoBodegas(bodegasResp.items)
        setCatalogoPuertos(puertosResp.items)
      } catch (err: any) {
        setMensaje(err?.message ?? 'Error cargando catálogos')
      } finally {
        setCargando(false)
      }
    })()
  }

  useEffect(() => {
    if (!token.trim()) return
    cargarCatalogos()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token])

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
          id_cliente: clienteId.trim() ? Number(clienteId) : undefined,
          id_tipo_producto: tipoProductoId.trim() ? Number(tipoProductoId) : undefined,
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
        const base = {
          id_cliente: Number(nuevo.id_cliente),
          id_tipo_producto: Number(nuevo.id_tipo_producto),
          cantidad: Number(nuevo.cantidad),
          fecha_registro: nuevo.fecha_registro,
          fecha_entrega: nuevo.fecha_entrega,
          precio_base: nuevo.precio_base,
          numero_guia: nuevo.numero_guia,
          tipo_envio: nuevo.tipo_envio,
        }

        const payload: CrearEnvioDTO =
          nuevo.tipo_envio === 'TERRESTRE'
            ? {
                ...base,
                id_bodega: Number(nuevo.id_bodega),
                placa_vehiculo: (nuevo.placa_vehiculo ?? '').trim(),
              }
            : {
                ...base,
                id_puerto: Number(nuevo.id_puerto),
                numero_flota: (nuevo.numero_flota ?? '').trim(),
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
      if (!esAdmin) {
        setMensaje('Se requiere rol admin')
        return
      }
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
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <button type="button" onClick={cargarCatalogos}>
            Cargar catálogos
          </button>
          <small>
            Clientes: {catalogoClientes.length} · Tipos: {catalogoTiposProducto.length} · Bodegas: {catalogoBodegas.length} · Puertos: {catalogoPuertos.length}
          </small>
        </div>

        <label>
          <span>Tipo envío</span>
          <select
            value={nuevo.tipo_envio}
            onChange={(e) => {
              const t = e.target.value as TipoEnvio
              if (t === 'TERRESTRE') {
                setNuevo({
                  ...nuevo,
                  tipo_envio: t,
                  id_bodega: nuevo.id_bodega ?? 1,
                  placa_vehiculo: nuevo.placa_vehiculo ?? 'ABC123',
                })
              } else {
                setNuevo({
                  ...nuevo,
                  tipo_envio: t,
                  id_puerto: nuevo.id_puerto ?? 1,
                  numero_flota: nuevo.numero_flota ?? 'ABC1234Z',
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
            <span>Cliente</span>
            <select
              value={nuevo.id_cliente}
              onChange={(e) => setNuevo({ ...nuevo, id_cliente: Number(e.target.value) })}
            >
              {catalogoClientes.length === 0 ? <option value={nuevo.id_cliente}>({nuevo.id_cliente})</option> : null}
              {catalogoClientes.map((c) => (
                <option key={c.id_cliente} value={c.id_cliente}>
                  {c.id_cliente} - {c.nombre}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span>Tipo producto</span>
            <select
              value={nuevo.id_tipo_producto}
              onChange={(e) => setNuevo({ ...nuevo, id_tipo_producto: Number(e.target.value) })}
            >
              {catalogoTiposProducto.length === 0 ? <option value={nuevo.id_tipo_producto}>({nuevo.id_tipo_producto})</option> : null}
              {catalogoTiposProducto.map((t) => (
                <option key={t.id_tipo_producto} value={t.id_tipo_producto}>
                  {t.id_tipo_producto} - {t.nombre}
                </option>
              ))}
            </select>
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
            <input value={String(nuevo.precio_base)} onChange={(e) => setNuevo({ ...nuevo, precio_base: e.target.value })} />
          </label>
          <small style={{ gridColumn: '1 / -1' }}>
            Descuento automático: si cantidad &gt; 10 → TERRESTRE 5% / MARITIMO 3%.
          </small>
        </div>

        {nuevo.tipo_envio === 'TERRESTRE' ? (
          <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
            <label>
              <span>Bodega</span>
              <select value={nuevo.id_bodega ?? 1} onChange={(e) => setNuevo({ ...nuevo, id_bodega: Number(e.target.value) })}>
                {catalogoBodegas.length === 0 ? <option value={nuevo.id_bodega ?? 1}>({nuevo.id_bodega ?? 1})</option> : null}
                {catalogoBodegas.map((b) => (
                  <option key={b.id_bodega} value={b.id_bodega}>
                    {b.id_bodega} - {b.nombre}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Placa vehículo</span>
              <input
                value={nuevo.placa_vehiculo ?? ''}
                onChange={(e) => setNuevo({ ...nuevo, placa_vehiculo: e.target.value.toUpperCase() })}
              />
            </label>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
            <label>
              <span>Puerto</span>
              <select value={nuevo.id_puerto ?? 1} onChange={(e) => setNuevo({ ...nuevo, id_puerto: Number(e.target.value) })}>
                {catalogoPuertos.length === 0 ? <option value={nuevo.id_puerto ?? 1}>({nuevo.id_puerto ?? 1})</option> : null}
                {catalogoPuertos.map((p) => (
                  <option key={p.id_puerto} value={p.id_puerto}>
                    {p.id_puerto} - {p.nombre}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Número flota</span>
              <input
                value={nuevo.numero_flota ?? ''}
                onChange={(e) => setNuevo({ ...nuevo, numero_flota: e.target.value.toUpperCase() })}
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
          <span>Cliente ID</span>
          <input value={clienteId} onChange={(e) => setClienteId(e.target.value)} placeholder="" />
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
          <span>Tipo producto ID</span>
          <input value={tipoProductoId} onChange={(e) => setTipoProductoId(e.target.value)} placeholder="" />
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
                <th style={{ textAlign: 'left' }}>Tipo producto</th>
                <th style={{ textAlign: 'left' }}>Cantidad</th>
                <th style={{ textAlign: 'left' }}>Precio base</th>
                <th style={{ textAlign: 'left' }}>Descuento</th>
                <th style={{ textAlign: 'left' }}>Precio final</th>
                <th style={{ textAlign: 'left' }}>Detalle</th>
                {esAdmin ? <th style={{ textAlign: 'left' }}>Acciones</th> : null}
              </tr>
            </thead>
            <tbody>
              {items.map((e) => (
                <tr key={e.id_envio}>
                  <td>{e.id_envio}</td>
                  <td>{e.numero_guia}</td>
                  <td>{e.tipo_envio}</td>
                  <td>{e.id_cliente}</td>
                  <td>{e.id_tipo_producto}</td>
                  <td>{e.cantidad}</td>
                  <td>{e.precio_base}</td>
                  <td>{e.descuento}</td>
                  <td>{e.precio_final}</td>
                  <td>
                    {e.tipo_envio === 'TERRESTRE'
                      ? `Bodega ${e.id_bodega ?? '-'} / ${e.placa_vehiculo ?? '-'}`
                      : `Puerto ${e.id_puerto ?? '-'} / ${e.numero_flota ?? '-'}`}
                  </td>
                  {esAdmin ? (
                    <td>
                      <button type="button" onClick={() => onEliminar(e.id_envio)}>
                        Eliminar
                      </button>
                    </td>
                  ) : null}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
