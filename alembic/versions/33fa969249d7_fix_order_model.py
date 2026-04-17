"""fix order model

Revision ID: 33fa969249d7
Revises: 200dc8901a9f
Create Date: 2026-04-16 12:29:01.245101

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "33fa969249d7"
down_revision: Union[str, Sequence[str], None] = "200dc8901a9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "courier_applications",
        sa.Column("id", sa.BigInteger(), nullable=False),  # ← String() → BigInteger()
        sa.Column(
            "user_id", sa.BigInteger(), nullable=False
        ),  # ← String() → BigInteger()
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("admin_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.alter_column(
        "orders",
        "status",
        existing_type=postgresql.ENUM(
            "CREATED",
            "ACCEPTED",
            "COOKING",
            "ON_THE_WAY",
            "DELIVERED",
            "CANCELED",
            name="orderstatus",
        ),
        type_=sa.String(),
        existing_nullable=False,
        existing_server_default=sa.text("'CREATED'::orderstatus"),
    )


def downgrade() -> None:
    op.alter_column(
        "orders",
        "status",
        existing_type=sa.String(),
        type_=postgresql.ENUM(
            "CREATED",
            "ACCEPTED",
            "COOKING",
            "ON_THE_WAY",
            "DELIVERED",
            "CANCELED",
            name="orderstatus",
        ),
        existing_nullable=False,
        existing_server_default=sa.text("'CREATED'::orderstatus"),
    )
    op.drop_table("courier_applications")
