"""Configuração de banco de dados."""

import logging
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

from app.config import settings

logger = logging.getLogger(__name__)

# Detectar se está em ambiente de teste
is_testing = (
    os.getenv("TEST_DATABASE_URL") is not None
    or settings.database_url == settings.test_database_url
    or "test" in settings.database_url.lower()
)

engine = create_engine(
    settings.test_database_url if is_testing else settings.database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    future=True,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)

Base = declarative_base()


def get_db() -> Generator:
    """Dependência para injetar sessão do banco nos endpoints."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao processar requisição no banco: {str(e)}")
        raise
    finally:
        db.close()


def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        raise
