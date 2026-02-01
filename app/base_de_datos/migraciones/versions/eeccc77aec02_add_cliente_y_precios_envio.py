"""add_cliente_y_precios_envio

Revision ID: eeccc77aec02
Revises: 5b2f0b57c3d1
Create Date: 2026-02-01 17:07:29.092540

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eeccc77aec02"
down_revision = "5b2f0b57c3d1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Tabla cliente
    op.create_table(
        "cliente",
        sa.Column("id_cliente", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("telefono", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id_cliente"),
    )
    op.create_index("ix_cliente_nombre", "cliente", ["nombre"], unique=False)

    # 2) Ajustes a envio: id_cliente + nuevos campos de precio
    op.add_column("envio", sa.Column("id_cliente", sa.Integer(), nullable=True))
    op.create_index("ix_envio_id_cliente", "envio", ["id_cliente"], unique=False)

    op.add_column("envio", sa.Column("precio_base", sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column("envio", sa.Column("descuento", sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column("envio", sa.Column("precio_final", sa.Numeric(precision=10, scale=2), nullable=True))

    # Migración de datos: si hay envíos existentes, crear un cliente por defecto y asignarlo.
    bind = op.get_bind()
    # En modo offline (alembic --sql) no hay conexión; omitimos migración de datos.
    if bind is not None:
        has_envios = False
        res = bind.execute(sa.text("SELECT 1 FROM envio LIMIT 1"))
        if res is not None:
            has_envios = res.first() is not None

        if has_envios:
            res_ins = bind.execute(
                sa.text(
                    "INSERT INTO cliente (nombre, email, telefono) "
                    "VALUES (:nombre, :email, :telefono) RETURNING id_cliente"
                ),
                {"nombre": "Cliente migrado", "email": None, "telefono": None},
            )
            if res_ins is not None:
                default_cliente_id = res_ins.scalar_one()
                bind.execute(sa.text("UPDATE envio SET id_cliente = :id_cliente"), {"id_cliente": default_cliente_id})

        # Convertir precio_envio -> precio_base/descuento/precio_final
        bind.execute(
            sa.text(
                "UPDATE envio "
                "SET precio_base = precio_envio, descuento = 0, precio_final = precio_envio "
                "WHERE precio_base IS NULL AND precio_final IS NULL"
            )
        )

    # Asegurar NOT NULL una vez migrados los datos
    op.alter_column("envio", "id_cliente", existing_type=sa.Integer(), nullable=False)
    op.alter_column(
        "envio",
        "precio_base",
        existing_type=sa.Numeric(precision=10, scale=2),
        nullable=False,
    )
    op.alter_column(
        "envio",
        "descuento",
        existing_type=sa.Numeric(precision=10, scale=2),
        nullable=False,
    )
    op.alter_column(
        "envio",
        "precio_final",
        existing_type=sa.Numeric(precision=10, scale=2),
        nullable=False,
    )

    # FK (solo después de haber poblado id_cliente)
    op.create_foreign_key(
        "fk_envio_cliente",
        source_table="envio",
        referent_table="cliente",
        local_cols=["id_cliente"],
        remote_cols=["id_cliente"],
    )

    # Constraint de precios
    op.create_check_constraint(
        "chk_envio_precio_final",
        "envio",
        "precio_final = precio_base - descuento",
    )

    # Limpiar esquema viejo
    op.drop_constraint("chk_envio_precio", "envio", type_="check")
    op.drop_column("envio", "precio_envio")


def downgrade() -> None:
    # Restaurar precio_envio desde precio_final
    op.add_column(
        "envio",
        sa.Column("precio_envio", sa.Numeric(precision=10, scale=2), nullable=True),
    )
    bind = op.get_bind()
    if bind is not None:
        bind.execute(sa.text("UPDATE envio SET precio_envio = precio_final WHERE precio_envio IS NULL"))
    op.alter_column(
        "envio",
        "precio_envio",
        existing_type=sa.Numeric(precision=10, scale=2),
        nullable=False,
    )
    op.create_check_constraint("chk_envio_precio", "envio", "precio_envio >= 0")

    # Quitar constraint y columnas nuevas
    op.drop_constraint("chk_envio_precio_final", "envio", type_="check")
    op.drop_constraint("fk_envio_cliente", "envio", type_="foreignkey")
    op.drop_index("ix_envio_id_cliente", table_name="envio")
    op.drop_column("envio", "precio_final")
    op.drop_column("envio", "descuento")
    op.drop_column("envio", "precio_base")
    op.drop_column("envio", "id_cliente")

    op.drop_index("ix_cliente_nombre", table_name="cliente")
    op.drop_table("cliente")
