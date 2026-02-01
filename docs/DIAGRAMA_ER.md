# Diagrama E-R (Mermaid)

> Nota: este diagrama está expresado en Mermaid `erDiagram` para que pueda renderizarse en GitHub/GitLab o en extensiones de VS Code.

```mermaid
erDiagram
  CLIENTE {
    int id_cliente PK
    string nombre
    string email
    string telefono
  }

  TIPO_PRODUCTO {
    int id_tipo_producto PK
    string nombre
  }

  BODEGA {
    int id_bodega PK
    string nombre
    string direccion
  }

  PUERTO {
    int id_puerto PK
    string nombre
    string ciudad
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
    string numero_guia UK
  }

  ENVIO_TERRESTRE {
    int id_envio PK, FK
    string placa_vehiculo
    int id_bodega FK
  }

  ENVIO_MARITIMO {
    int id_envio PK, FK
    string numero_flota
    int id_puerto FK
  }

  CLIENTE ||--o{ ENVIO : "tiene"
  TIPO_PRODUCTO ||--o{ ENVIO : "clasifica"

  ENVIO ||--o| ENVIO_TERRESTRE : "detalle"
  ENVIO ||--o| ENVIO_MARITIMO : "detalle"

  BODEGA ||--o{ ENVIO_TERRESTRE : "destino"
  PUERTO ||--o{ ENVIO_MARITIMO : "destino"
```

## Reglas de negocio (notas)

- Cada envío queda asociado a un cliente.
- Descuento automático si `cantidad > 10`:
  - Terrestre: 5% sobre `precio_base`.
  - Marítimo: 3% sobre `precio_base`.
- Se registra: `precio_base`, `descuento` y `precio_final`.
- Validaciones de formato:
  - `placa_vehiculo`: 3 letras + 3 números (ej: `ABC123`).
  - `numero_flota`: 3 letras + 4 números + 1 letra (ej: `ABC1234Z`).
  - `numero_guia`: alfanumérico único de 10 caracteres.
