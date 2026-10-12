# AI-Powered Data Engineering Agent

A reproducible **local data-engineering and AI observability prototype** with open source data, rule-driven Bronze/Silver/Gold Parquet transformations, DuckDB analytics, FastAPI backend, Streamlit frontend, Docker, pytest, GitHub Actions, open-weight Ollama integration and an Azure infrastructure example.

> **Status:** Code is committed. It has not been independently validated via live Docker/CI runs or provisioned in Azure. The "agent" is a constrained analytics/investigation workflow, not autonomous pipeline code authoring.

## Architecture

```text
UCI Iris (CC BY 4.0) -> Python validation -> Bronze Parquet
                                           -> Silver valid/rejected
                                           -> Gold DuckDB aggregates
                                                |
                                            JSON report
                                                |
                                      FastAPI metrics + AI
                                                |
                                        Streamlit dashboard
                                   Ollama optional (mock default)
```

## Open-source dataset

Included [UCI Iris](data/public/iris.csv), 150 rows, CC BY 4.0, DOI https://doi.org/10.24432/C56C76 . The data was normalized from the publicly accessible scikit-learn Iris dataset. See [source attribution](data/public/README.md).

## Windows setup

```powershell
git clone https://github.com/Khadija162/AI-Powered-Data-Engineering-Agent.git
cd AI-Powered-Data-Engineering-Agent
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m agent.pipeline
.\.venv\Scripts\python.exe -m pytest -q
```

Start backend and frontend in separate terminals:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

API docs: http://localhost:8000/docs
Dashboard: http://localhost:8501

Or, after running the ETL locally:

```powershell
docker compose up --build
```

The API container reads a **read-only** volume of the local pipeline report. Ports are localhost-only.

## Open-weight LLM

Mock investigation needs no API key or GPU. To use a locally hosted open-weight model, install [Ollama](https://ollama.com/) and run:

```powershell
ollama pull qwen2.5:3b
$env:AGENT_LLM_MODE="ollama"
$env:OLLAMA_MODEL="qwen2.5:3b"
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

This config applies to the **host-side backend**. The included Docker Compose file uses mock mode and does not implicitly connect to host Ollama. The LLM only explains quality evidence; it cannot rewrite production data, generate executable code or trigger pipelines.

## Azure cloud blueprint

Azure Data Factory / Event Hubs -> ADLS Gen2 -> Databricks Spark + Delta Lake Bronze/Silver/Gold -> operational metrics PostgreSQL -> FastAPI/Streamlit on Azure Container Apps -> open-weight model hosting (dedicated inference) -> Azure Monitor, Key Vault and Entra ID.

Terraform currently defines **only an Azure resource group and an ADLS Gen2 storage example**; no Azure services have been deployed. Review potential costs before provisioning.

## Folders

- `data/public/`: included open data and license provenance
- `agent/pipeline.py`: ETL and rule-based quality evidence
- `agent/llm.py`: mock/Ollama incident analyst
- `backend/`: API endpoints
- `frontend/`: Streamlit dashboard
- `tests/`: automated tests
- `infra/terraform/`: Azure storage starter
- `docs/`: architecture and implementation boundaries

**Safety:** The API is unauthenticated and unsuitable for public exposure as-is. Add identity, audit logs, quotas and secure secret management before deploying.
