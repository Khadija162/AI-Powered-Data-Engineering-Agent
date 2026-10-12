"""Rule-driven ingestion agent: Bronze/Silver/Gold + quality evidence, no arbitrary code execution."""
import json
from datetime import datetime, timezone
from pathlib import Path
import duckdb
import pandas as pd

COLUMNS=["sepal length (cm)","sepal width (cm)","petal length (cm)","petal width (cm)","target"]

def process(source="data/public/iris.csv",output="data",reports="artifacts"):
    frame=pd.read_csv(source)
    missing=set(COLUMNS)-set(frame.columns)
    if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
    root=Path(output)
    for layer in ("bronze","silver","gold"): (root/layer).mkdir(parents=True,exist_ok=True)
    frame.to_parquet(root/"bronze"/"events.parquet",index=False)
    nums=frame[COLUMNS].apply(pd.to_numeric,errors="coerce")
    valid=nums.notna().all(axis=1)&nums[COLUMNS[:4]].gt(0).all(axis=1)&nums["target"].isin([0,1,2])
    valid &= ~nums.duplicated(keep="first")
    clean=frame.loc[valid].copy()
    clean.to_parquet(root/"silver"/"valid.parquet",index=False)
    frame.loc[~valid].to_parquet(root/"silver"/"rejected.parquet",index=False)
    conn=duckdb.connect()
    try:
        metrics=conn.execute('SELECT target, count(*) AS records, avg("sepal length (cm)") AS mean_sepal_length FROM read_parquet(?) GROUP BY target ORDER BY target',[str((root/"silver"/"valid.parquet").as_posix())]).df()
    finally: conn.close()
    metrics.to_parquet(root/"gold"/"summary.parquet",index=False)
    report={"timestamp":datetime.now(timezone.utc).isoformat(),"rows":len(frame),"valid":len(clean),"rejected":int((~valid).sum()),"groups":len(metrics),"status":"review" if (~valid).sum()>0 else "passed"}
    dst=Path(reports)/"latest.json";dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report

if __name__=="__main__":print(process())
