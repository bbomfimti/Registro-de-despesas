"""create despesas table

Revision ID: 001_create_despesas
Revises:
Create Date: 2026-09-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_create_despesas"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "despesas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=100), nullable=False),
        sa.Column("descricao", sa.String(length=255), nullable=False),
        sa.Column("valor", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_despesas_id",
        "despesas",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_despesas_id",
        table_name="despesas",
    )

    op.drop_table("despesas")
