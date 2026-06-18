"""Schemas Pydantic para validação de entrada e saída."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    """Schema base de Produto."""

    nome: str = Field(..., min_length=3, max_length=100, description="Nome do produto")
    description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Descrição do produto",
    )
    preco: float = Field(..., gt=0, description="Preço do produto")
    estoque: int = Field(..., ge=0, description="Quantidade em estoque")
    ativo: bool = Field(default=True, description="Se o produto está ativo")


class ProdutoCreate(ProdutoBase):
    """Schema para criação de Produto."""

    pass


class ProdutoUpdate(BaseModel):
    """Schema para atualização de Produto."""

    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    preco: Optional[float] = Field(None, gt=0)
    estoque: Optional[int] = Field(None, ge=0)
    ativo: Optional[bool] = Field(None, description="Se o produto está ativo")


class ProdutoOut(BaseModel):
    """Schema para saída de Produto."""

    id: int = Field(..., description="ID único do produto")
    nome: str = Field(..., description="Nome do produto")
    description: str = Field(..., description="Descrição do produto")
    preco: float = Field(..., description="Preço do produto")
    estoque: int = Field(..., description="Quantidade em estoque")
    ativo: bool = Field(..., description="Se o produto está ativo")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data da última atualização")

    model_config = {
        "from_attributes": True
    }


class ProdutoListaOut(BaseModel):
    """Schema para listagem de Produtos."""

    total: int = Field(..., description="Total de produtos")
    produtos: list[ProdutoOut] = Field(..., description="Lista de produtos")
