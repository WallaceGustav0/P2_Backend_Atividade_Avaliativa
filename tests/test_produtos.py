"""Testes abrangentes para a API de Produtos."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi import status


# ============================================================================
# DADOS DE TESTE
# ============================================================================

PRODUTO_VALIDO = {
    "nome": "Teclado Mecânico",
    "description": "Teclado mecânico com switch azul de qualidade premium",
    "preco": 299.99,
    "estoque": 5,
    "ativo": True,
}

PRODUTO_VALIDO_2 = {
    "nome": "Mouse Gamer",
    "description": "Mouse gamer com DPI configurável e iluminação RGB",
    "preco": 199.99,
    "estoque": 15,
    "ativo": True,
}

# Payloads inválidos para teste parametrizado
PAYLOADS_INVALIDOS = [
    # Nome muito curto (< 3 caracteres)
    (
        {
            "nome": "AB",
            "description": "Descrição válida",
            "preco": 10.0,
            "estoque": 1,
            "ativo": True,
        },
        "nome",
    ),
    # Nome muito longo (> 100 caracteres)
    (
        {
            "nome": "A" * 101,
            "description": "Descrição válida",
            "preco": 10.0,
            "estoque": 1,
            "ativo": True,
        },
        "nome",
    ),
    # Descrição muito curta (< 5 caracteres)
    (
        {
            "nome": "Produto",
            "description": "Desc",
            "preco": 10.0,
            "estoque": 1,
            "ativo": True,
        },
        "description",
    ),
    # Descrição muito longa (> 500 caracteres)
    (
        {
            "nome": "Produto",
            "description": "D" * 501,
            "preco": 10.0,
            "estoque": 1,
            "ativo": True,
        },
        "description",
    ),
    # Preço negativo
    (
        {
            "nome": "Produto",
            "description": "Descrição válida",
            "preco": -10.0,
            "estoque": 1,
            "ativo": True,
        },
        "preco",
    ),
    # Preço zero
    (
        {
            "nome": "Produto",
            "description": "Descrição válida",
            "preco": 0.0,
            "estoque": 1,
            "ativo": True,
        },
        "preco",
    ),
    # Quantidade negativa
    (
        {
            "nome": "Produto",
            "description": "Descrição válida",
            "preco": 10.0,
            "estoque": -1,
            "ativo": True,
        },
        "estoque",
    ),
    # Campo obrigatório faltando (nome)
    (
        {
            "description": "Descrição válida",
            "preco": 10.0,
            "estoque": 1,
            "ativo": True,
        },
        "nome",
    ),
    # Campo obrigatório faltando (preco)
    (
        {
            "nome": "Produto",
            "description": "Descrição válida",
            "estoque": 1,
            "ativo": True,
        },
        "preco",
    ),
]


# ============================================================================
# TESTES OBRIGATÓRIOS CONFORME ESPECIFICAÇÃO
# ============================================================================


@pytest.mark.unit
def test_listar_produtos_vazio(client):
    """Testa listagem de produtos quando o banco está vazio."""
    response = client.get("/produtos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.unit
def test_criar_produto_persiste_no_banco(client):
    """Testa criação de produto e verifica persistência no banco."""
    response = client.post("/produtos", json=PRODUTO_VALIDO)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == PRODUTO_VALIDO["nome"]
    assert data["preco"] == PRODUTO_VALIDO["preco"]
    assert data["estoque"] == PRODUTO_VALIDO["estoque"]
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.unit
def test_criar_produto_aparece_na_listagem(client):
    """Testa que produto criado aparece na listagem."""
    client.post("/produtos", json=PRODUTO_VALIDO)
    response = client.get("/produtos")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == PRODUTO_VALIDO["nome"]


@pytest.mark.unit
def test_buscar_produto_por_id_sucesso(client, produto_existente):
    """Testa busca de produto por ID com sucesso."""
    produto_id = produto_existente["id"]
    response = client.get(f"/produtos/{produto_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == produto_id
    assert response.json()["nome"] == produto_existente["nome"]


@pytest.mark.unit
def test_buscar_produto_inexistente_retorna_404(client):
    """Testa busca de produto com ID inexistente retorna 404."""
    response = client.get("/produtos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_deletar_produto_retorna_204(client, produto_existente):
    """Testa deleção de produto retorna 204."""
    produto_id = produto_existente["id"]
    response = client.delete(f"/produtos/{produto_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.unit
def test_deletar_produto_confirma_remocao(client, produto_existente):
    """Testa que produto deletado não aparece mais na listagem."""
    produto_id = produto_existente["id"]

    # Deletar produto
    response_delete = client.delete(f"/produtos/{produto_id}")
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    # Confirmar que foi removido
    response_get = client.get(f"/produtos/{produto_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_deletar_produto_inexistente_retorna_404(client):
    """Testa deleção de produto inexistente retorna 404."""
    response = client.delete("/produtos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
@pytest.mark.parametrize("payload,_field", PAYLOADS_INVALIDOS)
def test_payloads_invalidos_retorna_422(client, payload, _field):
    """Testa validação de payloads inválidos retorna 422."""
    response = client.post("/produtos", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.unit
def test_isolamento_entre_testes(client):
    """Testa que cada teste tem banco limpo (isolamento)."""
    # Verificar que começa vazio
    response1 = client.get("/produtos")
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json() == []

    # Adicionar produto
    response2 = client.post("/produtos", json=PRODUTO_VALIDO)
    assert response2.status_code == status.HTTP_201_CREATED

    # Verificar que agora tem 1 produto
    response3 = client.get("/produtos")
    assert len(response3.json()) == 1


# ============================================================================
# TESTES ADICIONAIS (PARA MELHOR COBERTURA)
# ============================================================================


@pytest.mark.unit
def test_criar_multiplos_produtos(client):
    """Testa criação de múltiplos produtos e listagem ordenada."""
    # Criar 3 produtos
    response1 = client.post("/produtos", json=PRODUTO_VALIDO)
    response2 = client.post("/produtos", json=PRODUTO_VALIDO_2)
    response3 = client.post("/produtos", json={**PRODUTO_VALIDO, "nome": "Monitor"})

    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED
    assert response3.status_code == status.HTTP_201_CREATED

    # Listar todos
    response_list = client.get("/produtos")
    assert response_list.status_code == status.HTTP_200_OK
    assert len(response_list.json()) == 3


@pytest.mark.unit
def test_produto_com_quantidade_zero(client):
    """Testa criação de produto com quantidade zero (caso limite)."""
    produto = {
        "nome": "Produto Descontinuado",
        "description": "Produto sem estoque no momento",
        "preco": 50.0,
        "estoque": 0,
        "ativo": True,
    }
    response = client.post("/produtos", json=produto)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["estoque"] == 0


@pytest.mark.unit
def test_produto_com_preco_decimal(client):
    """Testa criação de produto com preço com muitas casas decimais."""
    produto = {
        "nome": "Produto Premium",
        "description": "Produto com preço em centavos",
        "preco": 99.99,
        "estoque": 1,
        "ativo": True,
    }
    response = client.post("/produtos", json=produto)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["preco"] == 99.99


@pytest.mark.unit
def test_atualizar_produto(client, produto_existente):
    """Testa atualização parcial de produto."""
    produto_id = produto_existente["id"]

    update_data = {
        "nome": "Caneca Atualizada",
        "preco": 49.99,
    }

    response = client.put(f"/produtos/{produto_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Caneca Atualizada"
    assert data["preco"] == 49.99
    assert data["estoque"] == produto_existente["estoque"]


@pytest.mark.unit
def test_atualizar_produto_inexistente(client):
    """Testa atualização de produto inexistente retorna 404."""
    response = client.put("/produtos/999", json={"nome": "Novo Nome"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_listar_com_paginacao(client, dois_produtos):
    """Testa listagem com skip e limit."""
    response = client.get("/produtos?skip=0&limit=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.unit
def test_headers_resposta_criacao(client):
    """Testa headers corretos na resposta de criação."""
    response = client.post("/produtos", json=PRODUTO_VALIDO)
    assert response.status_code == status.HTTP_201_CREATED
    assert "content-type" in response.headers
    assert "application/json" in response.headers["content-type"]


@pytest.mark.unit
def test_response_structure(client, produto_existente):
    """Testa que resposta tem estrutura correta."""
    response = client.get(f"/produtos/{produto_existente['id']}")
    data = response.json()

    required_fields = ["id", "nome", "description", "preco", "estoque", "ativo", "created_at", "updated_at"]
    for field in required_fields:
        assert field in data, f"Campo obrigatório faltando: {field}"


@pytest.mark.unit
def test_nome_produto_com_caracteres_especiais(client):
    """Testa criação de produto com caracteres especiais no nome."""
    produto = {
        "nome": "Produto & Serviço (Premium)",
        "description": "Produto com caracteres especiais: @, #, $, %, &",
        "preco": 100.0,
        "estoque": 5,
        "ativo": True,
    }
    response = client.post("/produtos", json=produto)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.unit
def test_descricao_com_quebras_linha(client):
    """Testa produto com descrição contendo quebras de linha."""
    produto = {
        "nome": "Produto Detalhado",
        "description": "Linha 1\nLinha 2\nLinha 3 com detalhes",
        "preco": 50.0,
        "estoque": 1,
        "ativo": True,
    }
    response = client.post("/produtos", json=produto)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.unit
def test_sequencia_create_read_update_delete(client):
    """Testa sequência completa: CREATE, READ, UPDATE, DELETE."""
    # CREATE
    create_response = client.post("/produtos", json=PRODUTO_VALIDO)
    assert create_response.status_code == status.HTTP_201_CREATED
    produto_id = create_response.json()["id"]

    # READ
    read_response = client.get(f"/produtos/{produto_id}")
    assert read_response.status_code == status.HTTP_200_OK

    # UPDATE
    update_response = client.put(
        f"/produtos/{produto_id}",
        json={"nome": "Produto Atualizado"},
    )
    assert update_response.status_code == status.HTTP_200_OK

    # DELETE
    delete_response = client.delete(f"/produtos/{produto_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar deleção
    final_response = client.get(f"/produtos/{produto_id}")
    assert final_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.unit
def test_produto_ativo_por_padrao(client):
    """Testa que produto criado tem ativo=True por padrão."""
    response = client.post("/produtos", json=PRODUTO_VALIDO)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["ativo"] is True


@pytest.mark.unit
def test_produto_com_ativo_false(client):
    """Testa criação de produto com ativo=False."""
    produto = {
        "nome": "Produto Inativo",
        "description": "Produto que não está disponível",
        "preco": 100.0,
        "estoque": 10,
        "ativo": False,
    }
    response = client.post("/produtos", json=produto)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["ativo"] is False


@pytest.mark.unit
def test_atualizar_status_ativo_produto(client, produto_existente):
    """Testa atualização do campo ativo de um produto."""
    produto_id = produto_existente["id"]
    
    # Verificar que começa como ativo
    assert produto_existente["ativo"] is True
    
    # Atualizar para inativo
    response = client.put(f"/produtos/{produto_id}", json={"ativo": False})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["ativo"] is False
    
    # Verificar que foi atualizado
    response_get = client.get(f"/produtos/{produto_id}")
    assert response_get.json()["ativo"] is False


@pytest.mark.unit
def test_health_check(client):
    """Testa endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"


@pytest.mark.unit
def test_root_endpoint(client):
    """Testa endpoint raiz."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
