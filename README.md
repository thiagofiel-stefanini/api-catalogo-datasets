# API Catálogo de Datasets

API REST simples para cadastrar e consultar os metadados dos datasets de uma equipe, feita em Python com FastAPI.

## Sobre

Em empresas grandes, os dados ficam espalhados em bancos, arquivos e data lakes, e muitas vezes ninguém sabe o que existe, onde está e quem é o responsável por cada base. Um catálogo de dados resolve esse problema guardando os metadados de cada dataset, ou seja, informações sobre os dados: nome, descrição, fonte, formato, camada e responsável.

Esta API é uma versão mínima desse catálogo, com as operações de cadastro, consulta, edição e remoção.

## Como executar

Pré-requisitos: Python 3.11 ou mais novo e Git.

1. Clone o repositório e entre na pasta:

   ```bash
   git clone https://github.com/thiagofiel-stefanini/api-catalogo-datasets.git
   cd api-catalogo-datasets
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate
   ```

   No PowerShell, o comando de ativação é `.venv\Scripts\Activate.ps1`. No Linux e no macOS, é `source .venv/bin/activate`.

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o servidor:

   ```bash
   uvicorn main:app --reload
   ```

5. Acesse a documentação interativa em http://127.0.0.1:8000/docs.
