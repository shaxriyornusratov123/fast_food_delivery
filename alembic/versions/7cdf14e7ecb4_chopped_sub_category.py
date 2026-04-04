"""chopped sub category

Revision ID: 7cdf14e7ecb4
Revises: e5f096c62945
Create Date: 2026-03-10 19:27:35.431760
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "7cdf14e7ecb4"
down_revision: Union[str, Sequence[str], None] = "e5f096c62945"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("products_subcategory_id_fkey", "products", type_="foreignkey")
    op.drop_column("products", "subcategory_id")
    op.drop_table("subcategories")
    op.add_column("products", sa.Column("category_id", sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, "products", "categories", ["category_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint(None, "products", type_="foreignkey")
    op.drop_column("products", "category_id")
    op.create_table(
        "subcategories",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("category_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"], ["categories.id"], name="subcategories_category_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="subcategories_pkey"),
    )
    op.add_column(
        "products",
        sa.Column("subcategory_id", sa.BIGINT(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "products_subcategory_id_fkey",
        "products",
        "subcategories",
        ["subcategory_id"],
        ["id"],
    )
