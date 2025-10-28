from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import Settings

engine = create_engine(Settings().DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_db_session():
    session = SessionLocal()

    try:
        yield session
        session.commit()
    finally:
        session.close()
