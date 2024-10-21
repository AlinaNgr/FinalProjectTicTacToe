import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app  # Adjust the import according to your project structure
from main import get_db
from main import Base, User

# Create a new database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create the database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)


# Test Login- endpoint
@pytest.fixture
def test_user():
    # Create a test user in the database
    db = TestingSessionLocal()
    user = User(username="testuser", password="password")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def test_login_success(test_user):
    response = client.post("/login", json={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert "games" in response.json()


def test_login_invalid_username():
    response = client.post("/login", json={"username": "invaliduser", "password": "password"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"


def test_login_invalid_password(test_user):
    response = client.post("/login", json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"


