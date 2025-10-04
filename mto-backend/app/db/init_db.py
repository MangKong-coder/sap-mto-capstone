from sqlalchemy.orm import Session

from app.core.logging import logger
from app.db.session import SessionLocal


def init_db() -> None:
    """
    Initialize the database with default data if needed.
    """
    db: Session = SessionLocal()
    try:
        logger.info("Initializing database...")
        # Add any initial data here
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        db.close()


