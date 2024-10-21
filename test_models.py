import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from main import Base, User, GameState


# Use SQLite in-memory database for testing
@pytest.fixture(scope='function')
def session():
    # Create an in-memory SQLite database engine
    engine = create_engine('sqlite:///:memory:')

    # Make sure the tables are created in the in-memory database
    Base.metadata.create_all(engine)

    # Create a new session bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Teardown: Clear the database schema and close the session
    session.close()
    clear_mappers()  # Clear the mappers after each test to avoid conflicts


def test_create_user(session):
    # Test user creation
    new_user = User(username='testuser', password='password123')
    session.add(new_user)
    session.commit()

    # Check if the user exists
    user = session.query(User).filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'
    assert user.password == 'password123'


def test_create_game_state(session):
    # Create a user
    new_user = User(username='testuser', password='password123')
    session.add(new_user)
    session.commit()

    # Test game state creation
    game_state = GameState(user_id=new_user.id, current_player='X')
    session.add(game_state)
    session.commit()

    # Check if the game state is related to the user
    game = session.query(GameState).filter_by(user_id=new_user.id).first()
    assert game is not None
    assert game.current_player == 'X'
    assert game.owner == new_user


def test_unique_username(session):
    # Create a user
    new_user1 = User(username='testuser', password='password123')
    session.add(new_user1)
    session.commit()

    # Try to create another user with the same username
    new_user2 = User(username='testuser', password='password456')
    session.add(new_user2)

    with pytest.raises(Exception):
        session.commit()
