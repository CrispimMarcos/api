import os
import sys
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Importações do app para as fixtures de integração
# O pytest.ini cuidará do PYTHONPATH, então 'app' deve ser encontrado
from app.main import app
from app.database import Base, get_db
from app.models.user_model import User # Necessário para o mock_db_session

# Carrega variáveis de ambiente.
# Se seu app/core/config.py já usa Pydantic BaseSettings para carregar o .env,
# esta linha pode ser redundante aqui, mas não causa problema.
load_dotenv()

# --- Fixture para mockar a sessão do banco de dados (para testes unitários) ---
@pytest.fixture
def mock_db_session():
    # Cria um mock para a sessão do SQLAlchemy
    db_session = MagicMock()
    # Configura o mock para que o .query() retorne um mock de query
    db_session.query.return_value = MagicMock()
    # Configura o mock para que o .filter() retorne o próprio mock de query (para encadeamento)
    db_session.query.return_value.filter.return_value = db_session.query.return_value
    # Configura o mock para que o .first() retorne None por padrão,
    # a menos que seja sobrescrito em um teste específico
    db_session.query.return_value.filter.return_value.first.return_value = None
    # Configura o mock para que o .all() retorne uma lista vazia por padrão
    db_session.query.return_value.all.return_value = []
    return db_session

# --- Fixtures para testes de integração ---

# URL do banco de dados de teste (garantir que está no .env)
DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://marcos:admin@localhost:5432/lu_estilo_test")

# Cria engine e sessionmaker para o banco de teste
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para criar e destruir o banco a cada função de teste (integração)
@pytest.fixture(scope="function")
def db_session_integration():
    # Cria todas as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        # Fornece a sessão do banco de dados para o teste
        yield db
    finally:
        # Fecha a sessão e remove todas as tabelas após o teste
        db.close()
        Base.metadata.drop_all(bind=engine)

# Fixture do client com override do get_db (para testes de integração)
@pytest.fixture(scope="function")
def client(db_session_integration):
    # Função que sobrescreve a dependência get_db do FastAPI
    def override_get_db():
        try:
            yield db_session_integration
        finally:
            # Não é necessário fechar a sessão aqui, pois db_session_integration
            # já cuida do ciclo de vida da sessão no finally dela.
            pass

    # Sobrescreve a dependência get_db com a nossa versão de teste
    app.dependency_overrides[get_db] = override_get_db
    # Fornece o TestClient para o teste
    yield TestClient(app)
    # Limpa as sobrescrições de dependência após o teste
    app.dependency_overrides.clear()
