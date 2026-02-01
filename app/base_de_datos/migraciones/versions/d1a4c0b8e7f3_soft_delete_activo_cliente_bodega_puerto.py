"""soft_delete_activo_cliente_bodega_puerto

Revision ID: d1a4c0b8e7f3
Revises: c8f1e2a3b4c5
Create Date: 2026-02-01

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d1a4c0b8e7f3"
down_revision = "c8f1e2a3b4c5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "cliente",
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "bodega",
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "puerto",
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("puerto", "activo")
    op.drop_column("bodega", "activo")
    op.drop_column("cliente", "activo")
