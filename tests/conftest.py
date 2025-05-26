import os
import sys
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

load_dotenv(dotenv_path=".env") 

# Garante que o diretório raiz do projeto está no path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações do app
from app.main import app
from app.database import Base, get_db

# --- Configuração do banco de dados ---
DATABASE_URL = "postgresql://postgres:fgOnRvJmJUHQECQNVQGRzNuocbuNGPsL@hopper.proxy.rlwy.net:46297/railway"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Cria e destrói as tabelas do banco de dados para cada teste.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente de teste com override de dependência do banco de dados.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
