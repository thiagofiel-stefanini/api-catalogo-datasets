from fastapi import FastAPI
from pydantic import BaseModel


class DatasetEntrada(BaseModel):
    """Dados que o cliente envia para cadastrar ou editar um dataset."""

    nome: str
    descricao: str
    fonte: str
    formato: str
    camada: str
    responsavel: str


class DatasetSaida(DatasetEntrada):
    """Dados que a API devolve: os mesmos campos de entrada, mais o id gerado pelo servidor."""

    id: int


app = FastAPI(
    title="API Catálogo de Datasets",
    description="API REST simples para cadastrar e consultar metadados de datasets.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
