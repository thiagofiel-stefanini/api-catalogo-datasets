from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


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
