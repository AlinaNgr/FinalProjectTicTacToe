from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()  # O singură instanță de FastAPI

# Add session middleware for handling sessions (using a secure random secret key)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# Restul codului rămâne neschimbat...


# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Security scheme pentru Swagger
security_scheme = {
    "sessionAuth": {
        "type": "apiKey",
        "in": "cookie",
        "name": "session",
        "description": "Autentificare cu sesiune"
    }
}


from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Generăm schema OpenAPI implicită
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API description",
        routes=app.routes,
    )

    # Asigură-te că 'components' există în schema generată
    if "components" in openapi_schema:
        # Eliminăm secțiunea de 'securitySchemes'
        openapi_schema["components"].pop("securitySchemes", None)

    # Eliminăm securitatea globală, dacă a fost setată
    openapi_schema.pop("security", None)

    # Salvăm schema OpenAPI modificată
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Aplicăm funcția customizată pentru OpenAPI la aplicația FastAPI
app.openapi = custom_openapi



