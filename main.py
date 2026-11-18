from fastapi import FastAPI

app = FastAPI(
    title="API Catálogo de Datasets",
    description="API REST simples para cadastrar e consultar metadados de datasets.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
