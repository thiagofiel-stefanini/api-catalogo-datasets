from fastapi import FastAPI, HTTPException, status
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


datasets: list[DatasetSaida] = [
    DatasetSaida(
        id=1,
        nome="vendas_2026",
        descricao="Vendas diárias por loja, usadas no dashboard de faturamento",
        fonte="Oracle",
        formato="csv",
        camada="bronze",
        responsavel="Time de Vendas",
    ),
    DatasetSaida(
        id=2,
        nome="clientes_ativos",
        descricao="Base de clientes com ao menos uma compra nos últimos 12 meses",
        fonte="PostgreSQL",
        formato="parquet",
        camada="prata",
        responsavel="Time de Marketing",
    ),
    DatasetSaida(
        id=3,
        nome="indicadores_financeiros",
        descricao="Indicadores consolidados para o relatório mensal da diretoria",
        fonte="S3",
        formato="json",
        camada="ouro",
        responsavel="Time Financeiro",
    ),
]


app = FastAPI(
    title="API Catálogo de Datasets",
    description="API REST simples para cadastrar e consultar metadados de datasets.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/datasets")
def listar_datasets() -> list[DatasetSaida]:
    """Lista todos os datasets cadastrados no catálogo."""
    return datasets


@app.get("/datasets/{dataset_id}")
def buscar_dataset(dataset_id: int) -> DatasetSaida:
    """Busca um dataset pelo id."""
    for dataset in datasets:
        if dataset.id == dataset_id:
            return dataset
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Dataset não encontrado"
    )


@app.post("/datasets")
def cadastrar_dataset(dataset: DatasetEntrada) -> DatasetSaida:
    """Cadastra um novo dataset no catálogo."""
    novo_id = len(datasets) + 1
    novo_dataset = DatasetSaida(id=novo_id, **dataset.model_dump())
    datasets.append(novo_dataset)
    return novo_dataset
