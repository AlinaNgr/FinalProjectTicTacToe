from main import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from main import User, GameState
from main import SessionLocal, engine
from main import get_game_state, get_user_by_username # Replace with the actual import path


# Configure test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture for setting up and tearing down the database
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)  # Create tables
    session = SessionLocal()
    yield session  # Provide the session to tests
    session.close()  # Close session after tests


# Test creating a user
def test_create_user(db):
    new_user = User(username="testuser", password="password123")
    db.add(new_user)
    db.commit()

    user = db.query(User).filter_by(username="testuser").first()
    assert user is not None
    assert user.username == "testuser"

# You can add other tests here as well


# Fixture for creating a temporary in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session  # Provide the session to tests
    session.close()  # Close the session after tests


def test_get_game_state(db):
    # Create a user and a game state to set up the test
    user = User(username="player1", password="password123")
    db.add(user)
    db.commit()
    db.refresh(user)  # Refresh to get the user ID

    # Create a game state associated with the user
    game_state = GameState(user_id=user.id, board='[[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]',
                           current_player="X")
    db.add(game_state)
    db.commit()
    db.refresh(game_state)  # Refresh to get the game state ID

    # Call the get_game_state function
    retrieved_game_state = get_game_state(db, user_id=user.id, game_id=game_state.id)

    # Assert that the retrieved game state matches the one we created
    assert retrieved_game_state is not None
    assert retrieved_game_state.id == game_state.id
    assert retrieved_game_state.user_id == game_state.user_id
    assert retrieved_game_state.board == game_state.board
    assert retrieved_game_state.current_player == game_state.current_player


def test_get_game_state_invalid_user(db):
    # Attempt to get a game state with a non-existent user
    retrieved_game_state = get_game_state(db, user_id=999, game_id=1)
    assert retrieved_game_state is None  # Should return None for invalid user ID


# Fixture for creating a temporary in-memory SQLite database for testing
@pytest.fixture(scope="function")
def db():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session  # Provide the session to tests
    session.close()  # Close the session after tests


def test_get_user_by_username(db):
    # Create a user to set up the test
    user = User(username="testuser", password="testpass")
    db.add(user)
    db.commit()
    db.refresh(user)  # Refresh to get the user ID

    # Call the get_user_by_username function
    retrieved_user = get_user_by_username(db, username="testuser")

    # Assert that the retrieved user matches the one we created
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.username == user.username
    assert retrieved_user.password == user.password  # Be cautious with password storage


def test_get_user_by_username_not_found(db):
    # Attempt to get a user that does not exist
    retrieved_user = get_user_by_username(db, username="nonexistentuser")
    assert retrieved_user is None  # Should return None for a non-existent username
