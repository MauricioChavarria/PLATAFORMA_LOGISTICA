"""create_usuario

Revision ID: c8f1e2a3b4c5
Revises: eeccc77aec02
Create Date: 2026-02-01 18:30:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c8f1e2a3b4c5"
down_revision = "eeccc77aec02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "usuario",
        sa.Column("id_usuario", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'user'"),
        ),
        sa.PrimaryKeyConstraint("id_usuario"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_usuario_username", "usuario", ["username"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_usuario_username", table_name="usuario")
    op.drop_table("usuario")
