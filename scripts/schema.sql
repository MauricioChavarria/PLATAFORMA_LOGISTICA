BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> cd7662f9d692

CREATE TABLE bodegas (
    id SERIAL NOT NULL, 
    nombre VARCHAR(160) NOT NULL, 
    ubicacion VARCHAR(255) NOT NULL, 
    pais VARCHAR(120) NOT NULL, 
    creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
    eliminado_en TIMESTAMP WITH TIME ZONE, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_bodegas_creado_en ON bodegas (creado_en);

CREATE INDEX ix_bodegas_eliminado_en ON bodegas (eliminado_en);

CREATE INDEX ix_bodegas_nombre ON bodegas (nombre);

CREATE INDEX ix_bodegas_pais ON bodegas (pais);

CREATE TABLE clientes (
    id SERIAL NOT NULL, 
    nombre VARCHAR(120) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    documento VARCHAR(32) NOT NULL, 
    telefono VARCHAR(32), 
    creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
    eliminado_en TIMESTAMP WITH TIME ZONE, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_clientes_creado_en ON clientes (creado_en);

CREATE UNIQUE INDEX ix_clientes_documento ON clientes (documento);

CREATE INDEX ix_clientes_eliminado_en ON clientes (eliminado_en);

CREATE UNIQUE INDEX ix_clientes_email ON clientes (email);

CREATE INDEX ix_clientes_nombre ON clientes (nombre);

CREATE TABLE productos (
    id SERIAL NOT NULL, 
    nombre VARCHAR(160) NOT NULL, 
    descripcion VARCHAR(500), 
    creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
    eliminado_en TIMESTAMP WITH TIME ZONE, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_productos_creado_en ON productos (creado_en);

CREATE INDEX ix_productos_eliminado_en ON productos (eliminado_en);

CREATE INDEX ix_productos_nombre ON productos (nombre);

CREATE TABLE puertos (
    id SERIAL NOT NULL, 
    nombre VARCHAR(160) NOT NULL, 
    pais VARCHAR(120) NOT NULL, 
    creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
    eliminado_en TIMESTAMP WITH TIME ZONE, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_puertos_creado_en ON puertos (creado_en);

CREATE INDEX ix_puertos_eliminado_en ON puertos (eliminado_en);

CREATE INDEX ix_puertos_nombre ON puertos (nombre);

CREATE INDEX ix_puertos_pais ON puertos (pais);

CREATE TABLE envios (
    id SERIAL NOT NULL, 
    cliente_id INTEGER NOT NULL, 
    producto_id INTEGER NOT NULL, 
    cantidad INTEGER NOT NULL, 
    fecha_registro DATE NOT NULL, 
    fecha_entrega DATE NOT NULL, 
    precio_base NUMERIC(14, 2) NOT NULL, 
    descuento NUMERIC(14, 2) NOT NULL, 
    precio_final NUMERIC(14, 2) NOT NULL, 
    numero_guia VARCHAR(64) NOT NULL, 
    tipo_envio VARCHAR(20) NOT NULL, 
    creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
    eliminado_en TIMESTAMP WITH TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(cliente_id) REFERENCES clientes (id), 
    FOREIGN KEY(producto_id) REFERENCES productos (id)
);

CREATE INDEX ix_envios_cliente_id ON envios (cliente_id);

CREATE INDEX ix_envios_creado_en ON envios (creado_en);

CREATE INDEX ix_envios_eliminado_en ON envios (eliminado_en);

CREATE UNIQUE INDEX ix_envios_numero_guia ON envios (numero_guia);

CREATE INDEX ix_envios_producto_id ON envios (producto_id);

CREATE INDEX ix_envios_tipo_envio ON envios (tipo_envio);

CREATE TABLE envios_maritimos (
    envio_id INTEGER NOT NULL, 
    puerto_id INTEGER NOT NULL, 
    numero_flota VARCHAR(32) NOT NULL, 
    PRIMARY KEY (envio_id), 
    FOREIGN KEY(envio_id) REFERENCES envios (id), 
    FOREIGN KEY(puerto_id) REFERENCES puertos (id)
);

CREATE INDEX ix_envios_maritimos_puerto_id ON envios_maritimos (puerto_id);

CREATE TABLE envios_terrestres (
    envio_id INTEGER NOT NULL, 
    bodega_id INTEGER NOT NULL, 
    placa_vehiculo VARCHAR(32) NOT NULL, 
    PRIMARY KEY (envio_id), 
    FOREIGN KEY(bodega_id) REFERENCES bodegas (id), 
    FOREIGN KEY(envio_id) REFERENCES envios (id)
);

CREATE INDEX ix_envios_terrestres_bodega_id ON envios_terrestres (bodega_id);

INSERT INTO alembic_version (version_num) VALUES ('cd7662f9d692') RETURNING alembic_version.version_num;

-- Running upgrade cd7662f9d692 -> 5b2f0b57c3d1

DROP TABLE envios_terrestres;

DROP TABLE envios_maritimos;

DROP TABLE envios;

DROP TABLE productos;

DROP TABLE clientes;

DROP TABLE bodegas;

DROP TABLE puertos;

CREATE TABLE tipo_producto (
    id_tipo_producto SERIAL NOT NULL, 
    nombre VARCHAR(50) NOT NULL, 
    PRIMARY KEY (id_tipo_producto), 
    UNIQUE (nombre)
);

CREATE TABLE bodega (
    id_bodega SERIAL NOT NULL, 
    nombre VARCHAR(100) NOT NULL, 
    direccion VARCHAR(200), 
    PRIMARY KEY (id_bodega)
);

CREATE TABLE puerto (
    id_puerto SERIAL NOT NULL, 
    nombre VARCHAR(100) NOT NULL, 
    ciudad VARCHAR(100), 
    PRIMARY KEY (id_puerto)
);

CREATE TABLE envio (
    id_envio SERIAL NOT NULL, 
    id_tipo_producto INTEGER NOT NULL, 
    cantidad INTEGER NOT NULL, 
    fecha_registro DATE NOT NULL, 
    fecha_entrega DATE NOT NULL, 
    precio_envio NUMERIC(10, 2) NOT NULL, 
    numero_guia VARCHAR(10) NOT NULL, 
    PRIMARY KEY (id_envio), 
    CONSTRAINT chk_envio_cantidad CHECK (cantidad > 0), 
    CONSTRAINT chk_envio_precio CHECK (precio_envio >= 0), 
    CONSTRAINT fk_envio_tipo_producto FOREIGN KEY(id_tipo_producto) REFERENCES tipo_producto (id_tipo_producto), 
    UNIQUE (numero_guia)
);

CREATE TABLE envio_terrestre (
    id_envio INTEGER NOT NULL, 
    placa_vehiculo VARCHAR(6) NOT NULL, 
    id_bodega INTEGER NOT NULL, 
    PRIMARY KEY (id_envio), 
    CONSTRAINT fk_terrestre_envio FOREIGN KEY(id_envio) REFERENCES envio (id_envio), 
    CONSTRAINT fk_terrestre_bodega FOREIGN KEY(id_bodega) REFERENCES bodega (id_bodega), 
    CONSTRAINT chk_placa CHECK (placa_vehiculo ~ '^[A-Z]{3}[0-9]{3}$')
);

CREATE TABLE envio_maritimo (
    id_envio INTEGER NOT NULL, 
    numero_flota VARCHAR(8) NOT NULL, 
    id_puerto INTEGER NOT NULL, 
    PRIMARY KEY (id_envio), 
    CONSTRAINT fk_maritimo_envio FOREIGN KEY(id_envio) REFERENCES envio (id_envio), 
    CONSTRAINT fk_maritimo_puerto FOREIGN KEY(id_puerto) REFERENCES puerto (id_puerto), 
    CONSTRAINT chk_flota CHECK (numero_flota ~ '^[A-Z]{3}[0-9]{4}[A-Z]$')
);

CREATE UNIQUE INDEX ix_tipo_producto_nombre ON tipo_producto (nombre);

CREATE INDEX ix_bodega_nombre ON bodega (nombre);

CREATE INDEX ix_puerto_nombre ON puerto (nombre);

CREATE UNIQUE INDEX ix_envio_numero_guia ON envio (numero_guia);

CREATE INDEX ix_envio_id_tipo_producto ON envio (id_tipo_producto);

CREATE INDEX ix_envio_terrestre_id_bodega ON envio_terrestre (id_bodega);

CREATE INDEX ix_envio_maritimo_id_puerto ON envio_maritimo (id_puerto);

UPDATE alembic_version SET version_num='5b2f0b57c3d1' WHERE alembic_version.version_num = 'cd7662f9d692';

-- Running upgrade 5b2f0b57c3d1 -> eeccc77aec02

CREATE TABLE cliente (
    id_cliente SERIAL NOT NULL, 
    nombre VARCHAR(100) NOT NULL, 
    email VARCHAR(100), 
    telefono VARCHAR(20), 
    PRIMARY KEY (id_cliente)
);

CREATE INDEX ix_cliente_nombre ON cliente (nombre);

ALTER TABLE envio ADD COLUMN id_cliente INTEGER;

CREATE INDEX ix_envio_id_cliente ON envio (id_cliente);

ALTER TABLE envio ADD COLUMN precio_base NUMERIC(10, 2);

ALTER TABLE envio ADD COLUMN descuento NUMERIC(10, 2);

ALTER TABLE envio ADD COLUMN precio_final NUMERIC(10, 2);

SELECT 1 FROM envio LIMIT 1;

UPDATE envio SET precio_base = precio_envio, descuento = 0, precio_final = precio_envio WHERE precio_base IS NULL AND precio_final IS NULL;

ALTER TABLE envio ALTER COLUMN id_cliente SET NOT NULL;

ALTER TABLE envio ALTER COLUMN precio_base SET NOT NULL;

ALTER TABLE envio ALTER COLUMN descuento SET NOT NULL;

ALTER TABLE envio ALTER COLUMN precio_final SET NOT NULL;

ALTER TABLE envio ADD CONSTRAINT fk_envio_cliente FOREIGN KEY(id_cliente) REFERENCES cliente (id_cliente);

ALTER TABLE envio ADD CONSTRAINT chk_envio_precio_final CHECK (precio_final = precio_base - descuento);

ALTER TABLE envio DROP CONSTRAINT chk_envio_precio;

ALTER TABLE envio DROP COLUMN precio_envio;

UPDATE alembic_version SET version_num='eeccc77aec02' WHERE alembic_version.version_num = '5b2f0b57c3d1';

COMMIT;

