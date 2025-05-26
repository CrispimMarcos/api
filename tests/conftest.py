# tests/conftest.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "postgresql://marcos:admin@localhost/lu_estilo"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():
    # Garante um estado limpo antes de criar as tabelas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(name="override_get_db")
def override_get_db_fixture(db_session):
    def _get_db_override():
        yield db_session
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()

@pytest.fixture(name="client")
def client(override_get_db):
    # Passa app como parâmetro posicional, não nomeado
    with TestClient(app) as client_instance:
        yield client_instance

@pytest.fixture(name="test_user_and_token")
def test_user_and_token_fixture(client: TestClient, db_session):
    from app.auth.auth_service import get_password_hash
    from app.models.user_model import User
    from app.auth.jwt_handler import create_access_token

    # Limpa usuários antes de criar o novo
    db_session.query(User).delete()
    db_session.commit()

    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hashed_password,
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token_data = {"sub": user.email, "role": user.role, "username": user.username}
    access_token = create_access_token(token_data)

    return {"user": user, "token": access_token}

@pytest.fixture(name="admin_user_and_token")
def admin_user_and_token_fixture(client: TestClient, db_session):
    from app.auth.auth_service import get_password_hash
    from app.models.user_model import User
    from app.auth.jwt_handler import create_access_token

    # Limpa usuários antes de criar o admin
    db_session.query(User).delete()
    db_session.commit()

    hashed_password = get_password_hash("adminpassword")
    admin_user = User(
        username="adminuser",
        email="admin@example.com",
        hashed_password=hashed_password,
        role="admin"
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)

    token_data = {"sub": admin_user.email, "role": admin_user.role, "username": admin_user.username}
    access_token = create_access_token(token_data)

    return {"user": admin_user, "token": access_token}
