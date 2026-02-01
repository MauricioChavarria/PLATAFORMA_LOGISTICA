"""nuevo_modelo_er

Revision ID: 5b2f0b57c3d1
Revises: cd7662f9d692
Create Date: 2026-02-01

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5b2f0b57c3d1"
down_revision = "cd7662f9d692"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # El modelo cambió sustancialmente. Para mantener el esquema consistente,
    # se eliminan tablas anteriores y se crean las nuevas según el DDL provisto.

    # Drop (orden por FKs)
    op.drop_table("envios_terrestres")
    op.drop_table("envios_maritimos")
    op.drop_table("envios")
    op.drop_table("productos")
    op.drop_table("clientes")
    op.drop_table("bodegas")
    op.drop_table("puertos")

    # Create nuevo E-R
    op.create_table(
        "tipo_producto",
        sa.Column("id_tipo_producto", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id_tipo_producto"),
        sa.UniqueConstraint("nombre"),
    )

    op.create_table(
        "bodega",
        sa.Column("id_bodega", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("direccion", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id_bodega"),
    )

    op.create_table(
        "puerto",
        sa.Column("id_puerto", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("ciudad", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id_puerto"),
    )

    op.create_table(
        "envio",
        sa.Column("id_envio", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id_tipo_producto", sa.Integer(), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("fecha_registro", sa.Date(), nullable=False),
        sa.Column("fecha_entrega", sa.Date(), nullable=False),
        sa.Column("precio_envio", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("numero_guia", sa.String(length=10), nullable=False),
        sa.CheckConstraint("cantidad > 0", name="chk_envio_cantidad"),
        sa.CheckConstraint("precio_envio >= 0", name="chk_envio_precio"),
        sa.ForeignKeyConstraint(
            ["id_tipo_producto"],
            ["tipo_producto.id_tipo_producto"],
            name="fk_envio_tipo_producto",
        ),
        sa.PrimaryKeyConstraint("id_envio"),
        sa.UniqueConstraint("numero_guia"),
    )

    op.create_table(
        "envio_terrestre",
        sa.Column("id_envio", sa.Integer(), nullable=False),
        sa.Column("placa_vehiculo", sa.String(length=6), nullable=False),
        sa.Column("id_bodega", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id_envio"], ["envio.id_envio"], name="fk_terrestre_envio"),
        sa.ForeignKeyConstraint(["id_bodega"], ["bodega.id_bodega"], name="fk_terrestre_bodega"),
        sa.CheckConstraint("placa_vehiculo ~ '^[A-Z]{3}[0-9]{3}$'", name="chk_placa"),
        sa.PrimaryKeyConstraint("id_envio"),
    )

    op.create_table(
        "envio_maritimo",
        sa.Column("id_envio", sa.Integer(), nullable=False),
        sa.Column("numero_flota", sa.String(length=8), nullable=False),
        sa.Column("id_puerto", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["id_envio"], ["envio.id_envio"], name="fk_maritimo_envio"),
        sa.ForeignKeyConstraint(["id_puerto"], ["puerto.id_puerto"], name="fk_maritimo_puerto"),
        sa.CheckConstraint("numero_flota ~ '^[A-Z]{3}[0-9]{4}[A-Z]$'", name="chk_flota"),
        sa.PrimaryKeyConstraint("id_envio"),
    )

    op.create_index("ix_tipo_producto_nombre", "tipo_producto", ["nombre"], unique=True)
    op.create_index("ix_bodega_nombre", "bodega", ["nombre"], unique=False)
    op.create_index("ix_puerto_nombre", "puerto", ["nombre"], unique=False)
    op.create_index("ix_envio_numero_guia", "envio", ["numero_guia"], unique=True)
    op.create_index("ix_envio_id_tipo_producto", "envio", ["id_tipo_producto"], unique=False)
    op.create_index("ix_envio_terrestre_id_bodega", "envio_terrestre", ["id_bodega"], unique=False)
    op.create_index("ix_envio_maritimo_id_puerto", "envio_maritimo", ["id_puerto"], unique=False)


def downgrade() -> None:
    # Downgrade a esquema anterior no soportado automáticamente.
    op.drop_index("ix_envio_maritimo_id_puerto", table_name="envio_maritimo")
    op.drop_index("ix_envio_terrestre_id_bodega", table_name="envio_terrestre")
    op.drop_index("ix_envio_id_tipo_producto", table_name="envio")
    op.drop_index("ix_envio_numero_guia", table_name="envio")
    op.drop_index("ix_puerto_nombre", table_name="puerto")
    op.drop_index("ix_bodega_nombre", table_name="bodega")
    op.drop_index("ix_tipo_producto_nombre", table_name="tipo_producto")

    op.drop_table("envio_maritimo")
    op.drop_table("envio_terrestre")
    op.drop_table("envio")
    op.drop_table("puerto")
    op.drop_table("bodega")
    op.drop_table("tipo_producto")
