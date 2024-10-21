import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from main import User
from main import UserCreate, Client
from main import create_user, get_user_by_username, get_current_user, get_db
from unittest.mock import MagicMock
from sqlalchemy.orm import Session


# Test pentru funcția get_user_by_username
def test_get_user_by_username():
    mock_db = MagicMock()
    mock_user = User(id=1, username="testuser", password="testpass")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    user = get_user_by_username(mock_db, "testuser")
    assert user == mock_user
    mock_db.query.return_value.filter.assert_called_once()

def test_create_user_success():
    mock_db = MagicMock()
    user_data = UserCreate(username="newuser", password="newpassword")

    # Simulăm că utilizatorul nu există în baza de date
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Simulăm crearea unui nou utilizator
    new_user = User(id=1, username=user_data.username, password=user_data.password)

    # Simulăm adăugarea utilizatorului în baza de date
    mock_db.add.side_effect = lambda x: setattr(x, 'id', new_user.id)

    # Executăm funcția create_user
    created_client = create_user(mock_db, user_data)

    # Verificăm rezultatul
    assert created_client.username == "newuser"
    assert created_client.user_id == 1  # Asigurăm că user_id este corect

    # Verificăm că utilizatorul a fost adăugat în baza de date
    assert mock_db.add.call_count == 2  # Verificăm că add a fost apelat o dată pentru utilizator și o dată pentru GameState

    # Verificăm că utilizatorul a fost creat cu datele corecte
    added_user = mock_db.add.call_args_list[0][0][0]  # Primul apel
    assert added_user.username == user_data.username
    assert added_user.password == user_data.password

    # Verificăm că commit și refresh au fost apelate o dată
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(added_user)


def test_create_user_username_already_exists():
    mock_db = MagicMock()
    user_data = UserCreate(username="existinguser", password="password")

    mock_db.query.return_value.filter.return_value.first.return_value = User(id=1, username="existinguser",
                                                                             password="password")

    with pytest.raises(HTTPException) as exc_info:
        create_user(mock_db, user_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Username already registered"


# Test pentru obținerea utilizatorului curent
def test_get_current_user():
    mock_request = MagicMock()
    mock_request.session = {"user_id": 1}

    mock_db = MagicMock()
    mock_user = User(id=1, username="testuser", password="testpass")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    user = get_current_user(mock_request, mock_db)

    assert user == mock_user
    mock_db.query.return_value.filter.assert_called_once()


def test_get_current_user_not_authenticated():
    mock_request = MagicMock()
    mock_request.session = {}

    mock_db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(mock_request, mock_db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"


def test_get_current_user_user_not_found():
    mock_request = MagicMock()
    mock_request.session = {"user_id": 1}

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(mock_request, mock_db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "User not found"

