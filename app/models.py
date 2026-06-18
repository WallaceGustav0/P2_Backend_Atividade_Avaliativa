"""Modelos de banco de dados."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from app.db import Base


class Produto(Base):
    """Modelo de Produto no banco de dados."""

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Produto(id={self.id}, nome='{self.nome}', preco={self.preco})>"
