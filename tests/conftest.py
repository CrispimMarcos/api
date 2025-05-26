import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import python_multipart
from app.main import app
from app.database import Base, get_db


@pytest.fixture
def client():
    return TestClient()

# URL do banco de dados de teste (ajuste conforme seu setup)
DATABASE_URL = "postgresql://marcos:admin@localhost:5432/lu_estilo"

# Cria engine e sessionmaker para o banco de teste
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Cria as tabelas antes de cada teste
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpa as tabelas depois do teste
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Override do get_db para usar o banco de teste
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
