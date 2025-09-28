from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
import os

# Get database URL from environment variable or use default from alembic.ini
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://neondb_owner:npg_5bN2zUaXMfxi@ep-round-tree-a12imzh0-pooler.ap-southeast-1.aws.neon.tech/mto-capstone?sslmode=require&channel_binding=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
