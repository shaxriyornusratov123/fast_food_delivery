"""fix status in order

Revision ID: 200dc8901a9f
Revises: fc3546d8ffde
Create Date: 2026-04-14 20:59:49.939870

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "200dc8901a9f"
down_revision: Union[str, Sequence[str], None] = "fc3546d8ffde"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    order_status_enum = sa.Enum(
        "CREATED",
        "ACCEPTED",
        "COOKING",
        "ON_THE_WAY",
        "DELIVERED",
        "CANCELED",
        name="orderstatus",
    )
    order_status_enum.create(op.get_bind(), checkfirst=True)

    # 1. Убираем дефолт
    op.alter_column(
        "orders",
        "status",
        existing_type=sa.VARCHAR(length=50),
        server_default=None,
        existing_nullable=False,
    )

    # 2. Обновляем существующие данные до UPPERCASE
    op.execute("""
        UPDATE orders SET status = UPPER(status)
        WHERE status IN ('created', 'accepted', 'cooking', 'on_the_way', 'delivered', 'canceled')
    """)

    # 3. Меняем тип
    op.alter_column(
        "orders",
        "status",
        existing_type=sa.VARCHAR(length=50),
        type_=order_status_enum,
        existing_nullable=False,
        postgresql_using="status::text::orderstatus",
    )

    # 4. Новый дефолт
    op.alter_column(
        "orders",
        "status",
        existing_type=order_status_enum,
        server_default="CREATED",
        existing_nullable=False,
    )
