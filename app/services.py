"""Camada de serviços para lógica de negócio de Produtos."""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.exceptions import ProdutoNaoEncontradoException
from app.models import Produto
from app.schemas import ProdutoCreate, ProdutoUpdate

logger = logging.getLogger(__name__)


class ProdutoService:
    """Serviço de gerenciamento de Produtos."""

    @staticmethod
    def criar_produto(db: Session, produto_data: ProdutoCreate) -> Produto:
        """Cria um novo produto no banco de dados."""
        logger.info(f"Criando produto: {produto_data.nome}")

        novo_produto = Produto(**produto_data.model_dump())
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)

        logger.info(f"Produto criado com sucesso: ID={novo_produto.id}")
        return novo_produto

    @staticmethod
    def obter_produto(db: Session, produto_id: int) -> Produto:
        """Obtém um produto pelo ID."""
        logger.debug(f"Buscando produto com ID: {produto_id}")

        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            logger.warning(f"Produto não encontrado: ID={produto_id}")
            raise ProdutoNaoEncontradoException()

        return produto

    @staticmethod
    def listar_produtos(db: Session, skip: int = 0, limit: int = 100) -> tuple[list[Produto], int]:
        """Lista todos os produtos com paginação."""
        logger.debug(f"Listando produtos (skip={skip}, limit={limit})")

        total = db.query(Produto).count()
        # Corrigido: order_by deve vir antes de offset e limit
        produtos = db.query(Produto).order_by(Produto.id).offset(skip).limit(limit).all()

        return produtos, total

    @staticmethod
    def atualizar_produto(db: Session, produto_id: int, produto_data: ProdutoUpdate) -> Produto:
        """Atualiza um produto existente."""
        logger.info(f"Atualizando produto: ID={produto_id}")

        produto = ProdutoService.obter_produto(db, produto_id)

        update_data = produto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(produto, field, value)

        db.add(produto)
        db.commit()
        db.refresh(produto)

        logger.info(f"Produto atualizado com sucesso: ID={produto_id}")
        return produto

    @staticmethod
    def deletar_produto(db: Session, produto_id: int) -> None:
        """Deleta um produto do banco de dados."""
        logger.info(f"Deletando produto: ID={produto_id}")

        produto = ProdutoService.obter_produto(db, produto_id)

        db.delete(produto)
        db.commit()

        logger.info(f"Produto deletado com sucesso: ID={produto_id}")

    @staticmethod
    def contar_produtos(db: Session) -> int:
        """Conta o total de produtos no banco."""
        return db.query(Produto).count()
