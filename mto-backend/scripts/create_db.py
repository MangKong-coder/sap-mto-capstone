"""
Script to create the database tables using Alembic migrations.
Run with: uv run python scripts/create_db.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import engine
from app.models import Base
from app.core.logging import logger


def create_tables():
    """Create all database tables."""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


if __name__ == "__main__":
    create_tables()


