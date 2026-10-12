import os
import requests
import streamlit as st
st.set_page_config(page_title="AI Data Engineering Agent",layout="wide")
st.title("AI Data Engineering · Control Center")
st.caption("Open research data · Validated Bronze/Silver/Gold ETL · Read-only AI investigation")
api=os.getenv("API_URL","http://localhost:8000")
try:
    r=requests.get(api+"/api/pipelines/latest",timeout=6);r.raise_for_status()
    report=r.json()["report"]
except (requests.RequestException,KeyError):report=None
if report:
    a,b,c=st.columns(3)
    a.metric("Source rows",report["rows"])
    b.metric("Validated",report["valid"])
    c.metric("Rejected",report["rejected"])
    st.write("Pipeline quality status:",report["status"])
    if st.button("Ask AI to investigate"):
        try:
            result=requests.post(api+"/api/agents/investigate",timeout=100)
            result.raise_for_status()
            st.json(result.json())
        except requests.RequestException as exc:st.error(str(exc))
else:st.info("No report available. Run python -m agent.pipeline before starting the app.")
