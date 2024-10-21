import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.open_api import setup_openapi  # Asigură-te că importul este corect


@pytest.fixture
def app():
    app = FastAPI()
    setup_openapi(app)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
    assert response.json()["info"]["title"] == "My API"
    assert response.json()["info"]["version"] == "1.0.0"


def test_security_scheme(client):
    response = client.get("/openapi.json")
    security_schemes = response.json().get("components", {}).get("securitySchemes", {})

    # Verificăm că securitySchemes este un dicționar
    assert isinstance(security_schemes, dict)

    # Verificăm că nu există 'sessionAuth' în securitySchemes
    assert "sessionAuth" not in security_schemes
