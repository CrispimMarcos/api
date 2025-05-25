from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# String de conexão com o banco (ajuste conforme seu banco e usuário)
SQLALCHEMY_DATABASE_URL = "postgresql://marcos:admin@localhost/lu_estilo"

# Cria o engine do SQLAlchemy (conexão com o banco)
engine = create_engine(settings.DATABASE_URL)

# Sessões para manipular transações e consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para herdar os models (tabelas)
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