from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://neondb_owner:npg_5bN2zUaXMfxi@ep-round-tree-a12imzh0-pooler.ap-southeast-1.aws.neon.tech/mto-capstone-simple?sslmode=require&channel_binding=require"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
