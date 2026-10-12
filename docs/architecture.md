# AI data engineering agent architecture

Implemented locally: UCI Iris open data, rules-based Bronze/Silver/Gold Parquet validation, DuckDB Gold aggregate, JSON pipeline report, FastAPI, Streamlit and opt-in Ollama open-weight LLM analyst (mock by default). Docker Compose and GitHub Actions CI are included.

Not implemented: autonomous pipeline authoring, data source discovery, code execution from LLM output, Spark/Delta streaming, cloud-deployed services, managed authentication or enterprise workflow engine. The LLM only explains facts and suggests investigations. No autonomous remediation or privileged actions.

Cloud plan: Azure Data Factory/Event Hubs ingestion -> ADLS Gen2 -> Azure Databricks + Delta Lake -> operational PostgreSQL -> Container Apps backend/frontend -> Azure AI endpoint or dedicated Ollama/vLLM compute -> Monitor and Key Vault. Terraform covers resource group/storage only and has not been applied.
