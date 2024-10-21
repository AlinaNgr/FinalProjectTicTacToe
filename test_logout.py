from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_logout():
    # Simulate a login request first
    login_response = client.post("/login", json={"username": "testuser", "password": "password"})

    # Check that the login was successful
    assert login_response.status_code == 200
    assert login_response.json()
    # Simulate a logout request
    logout_response = client.post("/logout")

    # Check if the logout response is as expected
    assert logout_response.status_code == 200
    assert logout_response.json() == {"message": "Logout successful"}


