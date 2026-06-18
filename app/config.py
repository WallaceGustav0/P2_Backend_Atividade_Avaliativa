"""Configuração centralizada da aplicação."""

import logging
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Banco de dados
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/db_dev",
    )
    test_database_url: str = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5433/db_test",
    )

    # Aplicação
    app_name: str = "API de Catálogo de Produtos"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


settings = Settings()


def setup_logging():
    """Configura logging da aplicação."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
