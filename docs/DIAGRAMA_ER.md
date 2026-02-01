# Diagrama Entidad-Relación (E-R)

```mermaid
erDiagram
  USUARIO {
    int id_usuario PK
    varchar username "UNIQUE"
    varchar password_hash
    varchar role
  }

  CLIENTE {
    int id_cliente PK
    varchar nombre
    varchar email
    varchar telefono
  }

  TIPO_PRODUCTO {
    int id_tipo_producto PK
    varchar nombre "UNIQUE"
  }

  BODEGA {
    int id_bodega PK
    varchar nombre
    varchar direccion
  }

  PUERTO {
    int id_puerto PK
    varchar nombre
    varchar ciudad
  }

  ENVIO {
    int id_envio PK
    int id_cliente FK
    int id_tipo_producto FK
    int cantidad
    date fecha_registro
    date fecha_entrega
    numeric precio_base
    numeric descuento
    numeric precio_final
    varchar numero_guia "UNIQUE"
  }

  ENVIO_TERRESTRE {
    int id_envio PK, FK
    varchar placa_vehiculo
    int id_bodega FK
  }

  ENVIO_MARITIMO {
    int id_envio PK, FK
    varchar numero_flota
    int id_puerto FK
  }

  CLIENTE ||--o{ ENVIO : "tiene"
  TIPO_PRODUCTO ||--o{ ENVIO : "clasifica"

  ENVIO ||--o| ENVIO_TERRESTRE : "detalle"
  ENVIO ||--o| ENVIO_MARITIMO : "detalle"

  BODEGA ||--o{ ENVIO_TERRESTRE : "origen"
  PUERTO ||--o{ ENVIO_MARITIMO : "origen"
```

## DBML (dbdiagram.io)

> Puedes pegar este bloque en https://dbdiagram.io para generar el diagrama automáticamente.

```dbml
Table usuario {
  id_usuario int [pk, increment]
  username varchar(50) [not null, unique]
  password_hash varchar(255) [not null]
  role varchar(20) [not null, default: 'user']

  Indexes {
    (username)
  }
}

Table cliente {
  id_cliente int [pk, increment]
  nombre varchar(100) [not null]
  email varchar(100)
  telefono varchar(20)

  Indexes {
    (nombre)
  }
}

Table tipo_producto {
  id_tipo_producto int [pk, increment]
  nombre varchar(50) [not null, unique]

  Indexes {
    (nombre)
  }
}

Table bodega {
  id_bodega int [pk, increment]
  nombre varchar(100) [not null]
  direccion varchar(200)

  Indexes {
    (nombre)
  }
}

Table puerto {
  id_puerto int [pk, increment]
  nombre varchar(100) [not null]
  ciudad varchar(100)

  Indexes {
    (nombre)
  }
}

Table envio {
  id_envio int [pk, increment]

  id_cliente int [not null]
  id_tipo_producto int [not null]

  cantidad int [not null, note: 'CHECK (cantidad > 0)']
  fecha_registro date [not null]
  fecha_entrega date [not null]

  precio_base numeric(10,2) [not null, note: 'CHECK (precio_base >= 0)']
  descuento numeric(10,2) [not null]
  precio_final numeric(10,2) [not null, note: 'CHECK (precio_final = precio_base - descuento)']

  numero_guia varchar(10) [not null, unique]

  Indexes {
    (id_cliente)
    (id_tipo_producto)
    (numero_guia)
  }
}

Table envio_terrestre {
  id_envio int [pk]
  placa_vehiculo varchar(6) [not null, note: "CHECK (placa_vehiculo ~ '^[A-Z]{3}[0-9]{3}$')"]
  id_bodega int [not null]

  Indexes {
    (id_bodega)
  }
}

Table envio_maritimo {
  id_envio int [pk]
  numero_flota varchar(8) [not null, note: "CHECK (numero_flota ~ '^[A-Z]{3}[0-9]{4}[A-Z]$')"]
  id_puerto int [not null]

  Indexes {
    (id_puerto)
  }
}

Ref: cliente.id_cliente < envio.id_cliente
Ref: tipo_producto.id_tipo_producto < envio.id_tipo_producto

Ref: bodega.id_bodega < envio_terrestre.id_bodega
Ref: puerto.id_puerto < envio_maritimo.id_puerto

Ref: envio.id_envio - envio_terrestre.id_envio
Ref: envio.id_envio - envio_maritimo.id_envio
```
