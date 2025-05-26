# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "strongpassword",
            "role": "user"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_register_duplicate_username(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "duplicateuser",
            "email": "first@example.com",
            "password": "password",
            "role": "user"
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "username": "duplicateuser",
            "email": "second@example.com",
            "password": "password",
            "role": "user"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username já registrado."

def test_register_duplicate_email(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "password",
            "role": "user"
        },
    )
    response = client.post(
        "/auth/register",
        json={
            "username": "user2",
            "email": "duplicate@example.com",
            "password": "password",
            "role": "user"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já registrado."

def test_login_user(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword",
            "role": "user"
        },
    )
    
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "loginpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas: username ou senha incorretos."

@pytest.mark.asyncio
async def test_refresh_token(client: TestClient, test_user_and_token: dict):
    token = test_user_and_token["token"]

    response = client.post(
        "/auth/refresh-token",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] != token

@pytest.mark.asyncio
async def test_refresh_token_invalid_token(client: TestClient):
    response = client.post(
        "/auth/refresh-token",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido ou expirado"