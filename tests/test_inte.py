import pytest
from unittest.mock import MagicMock, patch

# Importações das suas funções e modelos/schemas
from app.services.user_service import create_user, get_users
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserOut

# Importações para testar a rota de registro
from fastapi import HTTPException, status
from app.routers.auth_routes import register
from app.auth.auth_service import get_password_hash
from app.database import get_db # Esta dependência será mockada pela fixture


# --- Testes Unitários para Funções de Serviço de Usuário ---

# A fixture mock_db_session será automaticamente descoberta do conftest.py

def test_create_user_unit(mock_db_session):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123",
        hashed_password="hashed_password123",
        role="user"
    )

    mock_user_instance = MagicMock(spec=User)
    mock_user_instance.username = user_data.username
    mock_user_instance.email = user_data.email
    mock_user_instance.role = user_data.role
    mock_user_instance.id = 1

    mock_db_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    created_user = create_user(mock_db_session, user_data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(created_user)

    assert created_user.username == "testuser"
    assert created_user.email == "test@example.com"
    assert created_user.role == "user"
    assert created_user.id == 1

def test_get_users_unit(mock_db_session):
    mock_users = [
        MagicMock(spec=User, username="user1", email="user1@example.com"),
        MagicMock(spec=User, username="user2", email="user2@example.com")
    ]
    mock_db_session.query.return_value.all.return_value = mock_users

    users = get_users(mock_db_session)

    mock_db_session.query.assert_called_once_with(User)
    mock_db_session.query.return_value.all.assert_called_once()

    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].email == "user2@example.com"


# --- Testes Unitários para a Rota de Registro (Lógica de Negócio) ---

@patch('app.auth.auth_service.get_password_hash')
@patch('app.models.user_model.User')
@patch('app.database.get_db')
def test_register_user_unit(mock_get_db, mock_User_model, mock_get_password_hash):
    mock_db_session = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db_session

    mock_get_password_hash.return_value = "mocked_hashed_password"

    mock_User_instance = MagicMock(spec=User)
    mock_User_model.return_value = mock_User_instance

    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    user_data = UserCreate(
        username="newuser",
        email="new@example.com",
        password="securepassword",
        role="user"
    )

    registered_user = register(user_data, db=mock_db_session)

    mock_db_session.query.assert_called_with(User)
    assert mock_db_session.query.return_value.filter.call_count == 2

    mock_get_password_hash.assert_called_once_with("securepassword")
    mock_User_model.assert_called_once_with(
        username="newuser",
        email="new@example.com",
        hashed_password="mocked_hashed_password",
        role="user"
    )
    mock_db_session.add.assert_called_once_with(mock_User_instance)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_User_instance)

    assert registered_user.username == "newuser"
    assert registered_user.email == "new@example.com"
    assert registered_user.role == "user"

@patch('app.auth.auth_service.get_password_hash')
@patch('app.models.user_model.User')
@patch('app.database.get_db')
def test_register_user_username_exists_unit(mock_get_db, mock_User_model, mock_get_password_hash):
    mock_db_session = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db_session

    mock_db_session.query.return_value.filter.return_value.first.side_effect = [
        MagicMock(spec=User, username="existinguser"),
        None
    ]

    user_data = UserCreate(
        username="existinguser",
        email="new@example.com",
        password="securepassword",
        role="user"
    )

    with pytest.raises(HTTPException) as exc_info:
        register(user_data, db=mock_db_session)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Username já registrado."
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()

@patch('app.auth.auth_service.get_password_hash')
@patch('app.models.user_model.User')
@patch('app.database.get_db')
def test_register_user_email_exists_unit(mock_get_db, mock_User_model, mock_get_password_hash):
    mock_db_session = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db_session

    mock_db_session.query.return_value.filter.return_value.first.side_effect = [
        None,
        MagicMock(spec=User, email="existing@example.com")
    ]

    user_data = UserCreate(
        username="newuser",
        email="existing@example.com",
        password="securepassword",
        role="user"
    )

    with pytest.raises(HTTPException) as exc_info:
        register(user_data, db=mock_db_session)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Email já registrado."
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()
