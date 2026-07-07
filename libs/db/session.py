import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


MASTER_DATABASE_URL = os.getenv(
    "MASTER_DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5434/master_db",
)

engine = create_engine(MASTER_DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)


def get_session() -> Session:
    return SessionLocal()
