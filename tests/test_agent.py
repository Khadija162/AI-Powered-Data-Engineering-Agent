import pandas as pd
from fastapi.testclient import TestClient
from backend.main import app
from agent.pipeline import process
from agent.llm import explain

def test_validations(tmp_path):
    data=pd.DataFrame({"sepal length (cm)":[5.1,-1],"sepal width (cm)":[3.2,3.2],
      "petal length (cm)":[1.2,1.2],"petal width (cm)":[0.2,0.2],"target":[0,0]})
    f=tmp_path/"iris.csv";data.to_csv(f,index=False)
    result=process(str(f),str(tmp_path/"lake"),str(tmp_path/"reports"))
    assert result["rows"]==2 and result["rejected"]==1

def test_api(monkeypatch,tmp_path):
    monkeypatch.setenv("REPORT_PATH",str(tmp_path/"missing.json"))
    c=TestClient(app)
    assert c.get("/health").status_code==200
    assert c.post("/api/agents/investigate").status_code==404

def test_mock(monkeypatch):
    monkeypatch.setenv("AGENT_LLM_MODE","mock")
    assert explain({"rows":2,"valid":1,"rejected":1,"groups":1,"status":"review"})["human_review"]
