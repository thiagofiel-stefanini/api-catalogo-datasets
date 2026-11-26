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


def gerar_novo_id() -> int:
    """Gera o próximo id disponível, com base no maior id já usado na lista."""
    if not datasets:
        return 1
    return max(dataset.id for dataset in datasets) + 1


def localizar_indice_ou_404(dataset_id: int) -> int:
    """Retorna a posição do dataset na lista, ou lança 404 se o id não existir."""
    for indice, dataset in enumerate(datasets):
        if dataset.id == dataset_id:
            return indice
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Dataset não encontrado"
    )


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
    indice = localizar_indice_ou_404(dataset_id)
    return datasets[indice]


@app.post("/datasets", status_code=status.HTTP_201_CREATED)
def cadastrar_dataset(dataset: DatasetEntrada) -> DatasetSaida:
    """Cadastra um novo dataset no catálogo."""
    novo_id = gerar_novo_id()
    novo_dataset = DatasetSaida(id=novo_id, **dataset.model_dump())
    datasets.append(novo_dataset)
    return novo_dataset


@app.put("/datasets/{dataset_id}")
def editar_dataset(dataset_id: int, dataset: DatasetEntrada) -> DatasetSaida:
    """Edita um dataset existente, substituindo todos os seus campos."""
    indice = localizar_indice_ou_404(dataset_id)
    dataset_atualizado = DatasetSaida(id=dataset_id, **dataset.model_dump())
    datasets[indice] = dataset_atualizado
    return dataset_atualizado
