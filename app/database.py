import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependência para obter uma sessão do banco de dados.
    Fecha a sessão após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()