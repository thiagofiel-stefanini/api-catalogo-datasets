import pytest
from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


@pytest.fixture
def dataset_de_teste() -> dict:
    """Cadastra um dataset novo exclusivo para o teste e devolve o JSON cadastrado."""
    corpo = {
        "nome": "dataset_temporario",
        "descricao": "Dataset criado só para um teste automatizado",
        "fonte": "Teste",
        "formato": "csv",
        "camada": "bronze",
        "responsavel": "Suite de testes",
    }
    resposta = cliente.post("/datasets", json=corpo)
    return resposta.json()


def test_health_check_retorna_ok() -> None:
    """GET /health deve responder 200 com o status da API."""
    resposta = cliente.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_listar_datasets_retorna_os_exemplos() -> None:
    """GET /datasets deve responder 200 com os 3 datasets de exemplo."""
    resposta = cliente.get("/datasets")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_buscar_dataset_existente_retorna_200() -> None:
    """GET /datasets/{id} com um id existente deve responder 200 com o dataset certo."""
    resposta = cliente.get("/datasets/1")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "vendas_2026"


def test_buscar_dataset_inexistente_retorna_404() -> None:
    """GET /datasets/{id} com um id inexistente deve responder 404."""
    resposta = cliente.get("/datasets/999")
    assert resposta.status_code == 404


def test_cadastrar_dataset_retorna_201() -> None:
    """POST /datasets com dados válidos deve responder 201 e devolver o dataset com id."""
    corpo = {
        "nome": "dataset_novo",
        "descricao": "Dataset criado no teste de cadastro",
        "fonte": "Teste",
        "formato": "json",
        "camada": "ouro",
        "responsavel": "Suite de testes",
    }
    resposta = cliente.post("/datasets", json=corpo)
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "dataset_novo"
    assert "id" in resposta.json()


def test_cadastrar_dataset_sem_campo_obrigatorio_retorna_422() -> None:
    """POST /datasets sem um campo obrigatório deve responder 422."""
    corpo = {
        "nome": "dataset_incompleto",
        "fonte": "Teste",
        "formato": "csv",
        "camada": "bronze",
        "responsavel": "Suite de testes",
    }
    resposta = cliente.post("/datasets", json=corpo)
    assert resposta.status_code == 422


def test_editar_dataset_existente_retorna_200(dataset_de_teste: dict) -> None:
    """PUT /datasets/{id} em um id existente deve responder 200 com os dados atualizados."""
    dataset_id = dataset_de_teste["id"]
    corpo_atualizado = {
        "nome": "dataset_atualizado",
        "descricao": "Descrição atualizada pelo teste",
        "fonte": "Teste",
        "formato": "parquet",
        "camada": "prata",
        "responsavel": "Suite de testes",
    }
    resposta = cliente.put(f"/datasets/{dataset_id}", json=corpo_atualizado)
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "dataset_atualizado"
    assert resposta.json()["id"] == dataset_id


def test_editar_dataset_inexistente_retorna_404() -> None:
    """PUT /datasets/{id} com um id inexistente deve responder 404."""
    corpo = {
        "nome": "nao_importa",
        "descricao": "nao_importa",
        "fonte": "nao_importa",
        "formato": "csv",
        "camada": "bronze",
        "responsavel": "nao_importa",
    }
    resposta = cliente.put("/datasets/999", json=corpo)
    assert resposta.status_code == 404


def test_remover_dataset_existente_retorna_204(dataset_de_teste: dict) -> None:
    """DELETE /datasets/{id} em um id existente deve responder 204 e remover o dataset."""
    dataset_id = dataset_de_teste["id"]
    resposta = cliente.delete(f"/datasets/{dataset_id}")
    assert resposta.status_code == 204
    resposta_busca = cliente.get(f"/datasets/{dataset_id}")
    assert resposta_busca.status_code == 404


def test_remover_dataset_inexistente_retorna_404() -> None:
    """DELETE /datasets/{id} com um id inexistente deve responder 404."""
    resposta = cliente.delete("/datasets/999")
    assert resposta.status_code == 404
