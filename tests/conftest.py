"""Configuração de testes para Pytest."""

import os

# Definir DATABASE_URL antes de importar os módulos
os.environ.setdefault(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5433/db_test",
)

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.config import settings
from app.main import app

# Usar o banco de testes
engine = create_engine(
    settings.test_database_url,
    pool_pre_ping=True,
    future=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


def override_get_db():
    """Override da dependência get_db para usar o banco de testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Fixture que fornece uma sessão de teste limpa."""
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Fixture que fornece um cliente de teste com banco isolado."""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def produto_existente(client):
    """Fixture que cria um produto para testes."""
    payload = {
        "nome": "Caneca",
        "description": "Caneca personalizada de qualidade",
        "preco": 39.9,
        "estoque": 10,
        "ativo": True,
    }
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
def dois_produtos(client):
    """Fixture que cria dois produtos para testes."""
    produto1 = {
        "nome": "Teclado Mecânico",
        "description": "Teclado mecânico com switch azul de qualidade premium",
        "preco": 299.99,
        "estoque": 5,
        "ativo": True,
    }
    produto2 = {
        "nome": "Mouse Gamer",
        "description": "Mouse gamer com DPI configurável e RGB",
        "preco": 199.99,
        "estoque": 15,
        "ativo": True,
    }

    response1 = client.post("/produtos", json=produto1)
    response2 = client.post("/produtos", json=produto2)

    assert response1.status_code == 201
    assert response2.status_code == 201

    return [response1.json(), response2.json()]

