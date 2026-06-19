# 📦 API de Gerenciamento de Catálogo de Produtos

Esta é uma API REST de alta performance desenvolvida para o gerenciamento de produtos de um e-commerce. O projeto utiliza o ecossistema moderno do Python, integrando **FastAPI**, **SQLAlchemy 2.0**, **Pydantic v2** e **PostgreSQL**, com foco total em qualidade de código e testes automatizados.

---

## 📑 Índice
1. [Visão Geral](#visão-geral)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Configuração do Ambiente](#configuração-do-ambiente)
4. [Execução com Docker](#execução-com-docker)
5. [Testes Automatizados](#testes-automatizados)
6. [Isolamento de Testes](#isolamento-de-testes)
7. [Endpoints da API](#endpoints-da-api)
8. [Estrutura do Projeto](#estrutura-do-projeto)
9. [Conformidade Técnica](#conformidade-técnica)

---

## 🚀 Visão Geral

O projeto foi construído para atender a requisitos rigorosos de persistência de dados e validação. Ele permite o ciclo completo de CRUD (Create, Read, Update, Delete) de produtos, garantindo que cada operação seja validada tanto no nível de aplicação (Pydantic) quanto no nível de banco de dados (SQLAlchemy).

### ✅ Status Final do Projeto
*   **API:** 100% Funcional com 4 endpoints obrigatórios + Health Check.
*   **Qualidade:** 34 testes automatizados cobrindo casos positivos, negativos e de validação.
*   **Cobertura:** 91% de cobertura de código.
*   **Infraestrutura:** Dockerizado e pronto para deploy.

---

## 🛠 Tecnologias Utilizadas

*   **FastAPI:** Framework web moderno e rápido (high-performance).
*   **SQLAlchemy 2.0:** ORM para mapeamento e interação com o banco de dados.
*   **Pydantic v2:** Validação de dados e definição de schemas.
*   **PostgreSQL 15:** Banco de dados relacional robusto.
*   **Pytest:** Framework de testes automatizados.
*   **Docker & Docker Compose:** Orquestração de containers.

---

## ⚙️ Configuração do Ambiente

### 1. Requisitos Prévios
*   Python 3.11+
*   Docker e Docker Compose instalados.

### 2. Instalação das Dependências
Crie um ambiente virtual e instale as bibliotecas necessárias:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente
O projeto utiliza um arquivo `.env` para configurações. Você pode basear-se no `.env.example`:
```ini
DEBUG=True
LOG_LEVEL=INFO
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/db_dev
TEST_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/db_test
```

---

## 🐳 Execução com Docker

O projeto utiliza o Docker Compose para subir dois bancos de dados PostgreSQL independentes, garantindo que o ambiente de desenvolvimento não interfira no ambiente de testes.

### Instruções para subir o banco de teste:
Para executar a suíte de testes, você deve subir o container específico `db_test`:

```bash
# Sobe apenas o banco de testes em segundo plano
docker compose up -d db_test
```

Para subir o ambiente completo (API + Bancos):
```bash
docker compose up --build
```

---

## 🧪 Testes Automatizados

A suíte de testes foi desenhada para garantir a integridade de cada funcionalidade.

### Comando exato para executar os testes:
Para rodar os testes com detalhes de cada caso e relatório de cobertura:

```bash
docker compose up -d db_test; pytest -v --cov=app --cov-report=term-missing
```

### 📊 Saída Esperada do Pytest:
Abaixo está a representação da execução bem-sucedida dos 34 testes:

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.0, pluggy-1.6.0
rootdir: /home/ubuntu/Projeto_API_Produtos
configfile: pytest.ini
plugins: cov-7.1.0, anyio-4.8.0
collected 34 items

tests/test_produtos.py::test_listar_produtos_vazio PASSED                [  2%]
tests/test_produtos.py::test_criar_produto_persiste_no_banco PASSED      [  5%]
...
tests/test_produtos.py::test_payloads_invalidos_retorna_422 PASSED       [ 88%]
tests/test_produtos.py::test_health_check PASSED                         [ 97%]
tests/test_produtos.py::test_root_endpoint PASSED                        [100%]

---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
app/__init__.py         1      0   100%
app/config.py          14      0   100%
app/db.py              28     11    61%
app/exceptions.py      15      3    80%
app/main.py            45      2    96%
app/models.py          15      1    93%
app/schemas.py         30      0   100%
app/services.py        53      1    98%
---------------------------------------
TOTAL                 201     18    91%

======================== 34 passed, 56 warnings in 1.09s =======================
```
<img width="1253" height="357" alt="captura teste" src="https://github.com/user-attachments/assets/f6caa6d4-be09-4ceb-971e-ae1e48546a6e" />


---

## 🛡 Isolamento de Testes

O isolamento é um pilar fundamental deste projeto. Ele garante que cada teste comece com um estado "limpo", evitando que dados criados por um teste interfiram no resultado de outro.

### Como funciona no projeto:
1.  **Fixtures com Yield:** Utilizamos fixtures do Pytest no arquivo `conftest.py`.
2.  **Ciclo de Vida:** 
    *   **Setup:** Antes de cada função de teste, o comando `Base.metadata.create_all(bind=engine)` é executado, criando todas as tabelas do zero no banco de testes.
    *   **Execução:** O teste roda suas operações de forma independente.
    *   **Teardown:** Após a finalização do teste (independente de sucesso ou falha), o comando `Base.metadata.drop_all(bind=engine)` é executado, destruindo todas as tabelas e dados.
3.  **Dependency Injection:** O FastAPI permite substituir a sessão de banco de dados real pela sessão de teste através de `app.dependency_overrides`.

---

## 🔌 Endpoints da API

| Método | Rota | Status | Descrição |
| :--- | :--- | :--- | :--- |
| **GET** | `/produtos` | 200 | Lista todos os produtos cadastrados. |
| **POST** | `/produtos` | 201 | Cria um novo produto (Valida nome, preço e estoque). |
| **GET** | `/produtos/{id}` | 200/404 | Busca um produto específico pelo ID único. |
| **PUT** | `/produtos/{id}` | 200/404 | Atualiza dados de um produto existente. |
| **DELETE** | `/produtos/{id}` | 204/404 | Remove permanentemente um produto do catálogo. |
| **GET** | `/health` | 200 | Verifica se a API e o banco estão operacionais. |

---

## 📂 Estrutura do Projeto

```text
Projeto_API_Produtos/
├── app/
│   ├── main.py          # Ponto de entrada (FastAPI + Lifespan)
│   ├── config.py        # Configurações via Pydantic Settings
│   ├── db.py            # Configuração do SQLAlchemy e Sessão
│   ├── models.py        # Definição das tabelas (ORM)
│   ├── schemas.py       # Validação de dados (Pydantic v2)
│   ├── exceptions.py    # Tratamento de erros customizados
│   └── services.py      # Lógica de negócio e CRUD
├── tests/
│   ├── conftest.py      # Configuração de Fixtures e Isolamento
│   └── test_produtos.py # Suíte de 34 testes automatizados
├── docker-compose.yml   # Orquestração de serviços PostgreSQL
├── Dockerfile           # Build otimizado da aplicação
├── pytest.ini           # Configurações do Pytest
└── requirements.txt     # Dependências do projeto
```

---

## 📝 Conformidade Técnica

Este projeto foi desenvolvido seguindo 100% das especificações:
*   **PostgreSQL via Docker:** Sem uso de SQLite em memória para os testes finais.
*   **Validação Rigorosa:** Campos como `nome`, `preco` (>0) e `estoque` (>=0) são validados via Pydantic.
*   **Status Codes:** Uso correto de 201 (Created), 204 (No Content), 404 (Not Found) e 422 (Unprocessable Entity).

---
