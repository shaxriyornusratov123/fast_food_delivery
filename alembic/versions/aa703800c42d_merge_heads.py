"""merge heads

Revision ID: aa703800c42d
Revises: 59aa33354f96, f0b527d5ca28
Create Date: 2026-03-04 14:32:18.434068

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "aa703800c42d"
down_revision: Union[str, Sequence[str], None] = ("59aa33354f96", "f0b527d5ca28")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
