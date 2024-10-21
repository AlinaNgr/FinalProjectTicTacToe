import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app  # Adjust the import according to your app's structure
from main import User, GameState
from main import get_db
from main import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use an in-memory database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the dependency to use the testing database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Mock the get_current_user function
def mock_get_current_user():
    return User(username="testuser", id=1)  # Mock a user object directly


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def setup_db():
    from main import Base  # Import your Base model to create tables
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)  # Clean up after tests


def create_test_user(db):
    test_user = User(username="testuser", password="testpass")  # Adjust as needed
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    return test_user


def test_run_game_new_game(client, setup_db):
    db = TestingSessionLocal()
    create_test_user(db)  # Create the user

    response = client.get("/run-game/1")  # Directly access the endpoint

    assert response.status_code == 200
    data = response.json()
    assert data["board"] == [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    assert data["current_player"] == "X"
