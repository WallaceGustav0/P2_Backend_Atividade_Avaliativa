"""Aplicação FastAPI principal."""

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings, setup_logging
from app.db import get_db, init_db
from app.schemas import ProdutoCreate, ProdutoOut, ProdutoUpdate
# Importar ProdutoListaOut se necessário no futuro
from app.services import ProdutoService

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação."""
    logger.info(f"Iniciando {settings.app_name} v{settings.app_version}")
    init_db()
    yield
    logger.info("Encerrando aplicação")


# Criar aplicação
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para gerenciamento de catálogo de produtos",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Adicionar CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def read_root():
    """Endpoint raiz."""
    return {
        "message": "Bem-vindo à API de Catálogo de Produtos",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["health"])
def health_check():
    """Verifica a saúde da aplicação."""
    return {"status": "ok", "app": settings.app_name}


@app.post(
    "/produtos",
    response_model=ProdutoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar produto",
    description="Cria um novo produto no catálogo",
)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
):
    """Cria um novo produto."""
    return ProdutoService.criar_produto(db, produto)


@app.get(
    "/produtos",
    response_model=list[ProdutoOut],
    status_code=status.HTTP_200_OK,
    summary="Listar produtos",
    description="Lista todos os produtos do catálogo",
)
def listar_produtos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Lista todos os produtos."""
    produtos, _ = ProdutoService.listar_produtos(db, skip, limit)
    return produtos


@app.get(
    "/produtos/{produto_id}",
    response_model=ProdutoOut,
    status_code=status.HTTP_200_OK,
    summary="Obter produto",
    description="Obtém detalhes de um produto específico",
)
def obter_produto(
    produto_id: int,
    db: Session = Depends(get_db),
):
    """Obtém um produto pelo ID."""
    return ProdutoService.obter_produto(db, produto_id)


@app.put(
    "/produtos/{produto_id}",
    response_model=ProdutoOut,
    status_code=status.HTTP_200_OK,
    summary="Atualizar produto",
    description="Atualiza um produto existente",
)
def atualizar_produto(
    produto_id: int,
    produto: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza um produto existente."""
    return ProdutoService.atualizar_produto(db, produto_id, produto)


@app.delete(
    "/produtos/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar produto",
    description="Remove um produto do catálogo",
)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
):
    """Deleta um produto."""
    ProdutoService.deletar_produto(db, produto_id)
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
