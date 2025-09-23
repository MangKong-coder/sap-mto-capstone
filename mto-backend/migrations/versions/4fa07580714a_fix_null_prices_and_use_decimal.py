"""fix_null_prices_and_use_decimal

Revision ID: 4fa07580714a
Revises: 0311eb10f098
Create Date: 2025-09-24 03:58:41.026156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fa07580714a'
down_revision: Union[str, Sequence[str], None] = '0311eb10f098'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Fix NULL prices by setting them to 0.0
    op.execute("UPDATE products SET price = 0.0 WHERE price IS NULL")
    
    # Change price column from Float to DECIMAL(10, 2)
    op.alter_column('products', 'price',
                   existing_type=sa.Float(),
                   type_=sa.DECIMAL(10, 2),
                   nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert price column back to Float
    op.alter_column('products', 'price',
                   existing_type=sa.DECIMAL(10, 2),
                   type_=sa.Float(),
                   nullable=False)
