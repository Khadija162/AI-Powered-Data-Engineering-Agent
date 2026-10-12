"""Read-only analytics and explanation API; no user-triggered server commands."""
import os
import json
from pathlib import Path
import requests
from fastapi import FastAPI,HTTPException
from agent.llm import explain
app=FastAPI(title="AI Data Engineering Agent",version="0.1.0")

def report():
    path=Path(os.getenv("REPORT_PATH","artifacts/latest.json"))
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None

@app.get("/health")
def health():return {"status":"ok","report_ready":report() is not None}

@app.get("/api/pipelines/latest")
def latest():return {"report":report()}

@app.post("/api/agents/investigate")
def investigate():
    current=report()
    if not current:raise HTTPException(404,"Run the data pipeline first")
    try:return explain(current)
    except (requests.RequestException,KeyError,ValueError) as exc:raise HTTPException(502,"LLM inference unavailable") from exc
