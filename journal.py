"""ASCEND V9 prospective, close-to-close paper research journal.

Signals are recorded at session close; entry is the NEXT session's adjusted close,
not a tradeable guaranteed fill. No lookahead and no brokerage integration.
"""
import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf
from performance_lab import summarize
from risk_lab import evaluate as evaluate_risk
from audit_lab import record_metadata, daily_marks

PATH=Path("data/performance.json")
COST_BPS=10 # round-trip friction, illustrative, applied once at exit
HORIZONS=(2,5)
def series(ticker):
    d=yf.download(ticker,period="2y",interval="1d",auto_adjust=True,progress=False,threads=False)
    if d.empty:return None
    c=d["Close"].squeeze().dropna().astype(float)
    c.index=pd.to_datetime(c.index).tz_localize(None).normalize()
    return c
def load():
    try:
        d=json.loads(PATH.read_text())
        if d.get("schema")==1 and isinstance(d.get("records"),list):return d
    except (FileNotFoundError,ValueError,TypeError):pass
    return {"schema":1,"records":[]}
def update(snapshot):
    data=load();records=data["records"]
    # Evaluate ONLY entries already present in previous published journal.
    tickers={p["ticker"] for r in records for p in r.get("picks",[])}
    cache={t:series(t) for t in sorted(tickers|{"SPY"})}
    for record in records:
        signal=pd.Timestamp(record["signal_date"])
        bench=cache.get("SPY")
        for p in record["picks"]:
            c=cache.get(p["ticker"])
            if c is None or bench is None:continue
            aligned=pd.concat([c.rename("stock"),bench.rename("spy")],axis=1).dropna()
            # The next common session after the signal is an observable close-based proxy.
            future=aligned.loc[aligned.index>signal]
            if future.empty:continue
            entry=future.iloc[0];p.setdefault("entry_date",future.index[0].date().isoformat())
            p.setdefault("entry_price",round(float(entry["stock"]),4))
            p.setdefault("benchmark_entry",round(float(entry["spy"]),4))
            # Avoid silently changing entry on a subsequent download.
            if p["entry_date"]!=future.index[0].date().isoformat():continue
            for horizon in HORIZONS:
                key=str(horizon)
                if key in p.setdefault("outcomes",{}):continue
                if len(future)<=horizon:continue
                end=future.iloc[horizon]
                gross=float(end["stock"]/entry["stock"]-1)
                benchmark=float(end["spy"]/entry["spy"]-1)
                net=gross-COST_BPS/10000
                p["outcomes"][key]={"exit_date":future.index[horizon].date().isoformat(),"gross_pct":round(gross*100,3),"net_pct":round(net*100,3),"spy_pct":round(benchmark*100,3),"excess_net_pct":round((net-benchmark)*100,3)}
    # A unique session prevents repeated manual runs from fabricating independent observations.
    if snapshot.get("status")=="ok" and len(snapshot.get("picks",[]))==5:
        day=snapshot["price_as_of"]
        if day and not any(r["signal_date"]==day for r in records):
            records.append({"signal_date":day,"captured_at":datetime.now(timezone.utc).isoformat(),"strategy":record_metadata(snapshot),"picks":[{"ticker":p["ticker"],"rank":p["rank"],"outcomes":{}} for p in snapshot["picks"]]})
    records.sort(key=lambda r:r["signal_date"])
    data["records"]=records
    data["updated_at"]=datetime.now(timezone.utc).isoformat()
    data["method"]="Signals recorded after closing data; next common session adjusted close is hypothetical entry; 2/5 subsequent sessions, 10 bps illustrative round-trip cost; no execution."
    summary={}
    for h in HORIZONS:
        vals=[p["outcomes"][str(h)] for r in records for p in r["picks"] if str(h) in p.get("outcomes",{})]
        summary[str(h)]={"observations":len(vals),"average_net_pct":round(sum(x["net_pct"] for x in vals)/len(vals),3) if vals else None,"average_excess_vs_spy_pct":round(sum(x["excess_net_pct"] for x in vals)/len(vals),3) if vals else None,"positive_fraction":round(sum(x["net_pct"]>0 for x in vals)/len(vals),3) if vals else None}
    data["summary"]=summary
    data["cohorts"]={str(h):summarize(records,h) for h in HORIZONS}
    data["risk"]={str(h):evaluate_risk(records,h) for h in HORIZONS}
    data["daily_marks"]=daily_marks(records,cache,5)
    PATH.parent.mkdir(parents=True,exist_ok=True)
    PATH.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")
    return {"status":"tracking","signal_days":len(records),"summary":summary,"cohorts":data["cohorts"],"risk":data["risk"],"daily_marks":{"status":data["daily_marks"]["status"],"cohorts_with_marks":data["daily_marks"].get("cohorts_with_marks",0),"recent_paths":data["daily_marks"].get("paths",[])[-5:],"note":data["daily_marks"].get("note")},"method":data["method"]}
