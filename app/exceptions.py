"""Exceções customizadas da aplicação."""

from fastapi import HTTPException, status


class ProdutoException(HTTPException):
    """Exceção base para erros de produto."""

    pass


class ProdutoNaoEncontradoException(ProdutoException):
    """Produto não encontrado."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )


class ProdutoJaExisteException(ProdutoException):
    """Produto já existe no banco."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Produto já existe",
        )


class DadosInvalidosException(ProdutoException):
    """Dados inválidos fornecidos."""

    def __init__(self, detail: str = "Dados inválidos"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class ErroInternoException(ProdutoException):
    """Erro interno da aplicação."""

    def __init__(self, detail: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
