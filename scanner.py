"""ASCEND v1: conservative, transparent momentum research prototype.
Not a predictive AI or validated trading recommendation engine.
Requires live daily bars; on failure publishes no picks.
"""
import json, math, os
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import yfinance as yf

UNIVERSE = ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","AVGO","AMD","TSM","COST","JPM","V","MA","UNH","LLY","XOM","CAT","GE","ORCL","NFLX","CRM","ADBE","QCOM","TXN","AMAT","MU","UBER","PANW","NOW","WMT"]
OUTPUT=Path("data/latest.json")
def main():
    now=datetime.now(timezone.utc).isoformat()
    result={"status":"unavailable","generated_at":now,"price_as_of":None,"method":"20-day trend + 5-day momentum, volatility and liquidity filters (experimental)","picks":[],"message":"Insufficient fresh, verified market data."}
    try:
        candidates=[]
        for ticker in UNIVERSE:
            try:
                frame=yf.download(ticker,period="4mo",interval="1d",auto_adjust=True,progress=False,threads=False)
                if frame.empty or len(frame)<45: continue
                close=frame["Close"].squeeze().dropna()
                volume=frame["Volume"].squeeze().reindex(close.index)
                if len(close)<45 or close.iloc[-1]<=0:continue
                date=close.index[-1]
                age=(pd.Timestamp.now(tz="UTC")-pd.Timestamp(date).tz_localize("UTC") if pd.Timestamp(date).tzinfo is None else pd.Timestamp.now(tz="UTC")-pd.Timestamp(date)).days
                if age>5:continue
                price=float(close.iloc[-1])
                liquidity=float((close.tail(20)*volume.tail(20)).mean())
                if price<5 or liquidity<20_000_000:continue
                momentum=float((price/float(close.iloc[-6])-1)*100)
                trend=float((price/float(close.iloc[-21])-1)*100)
                vol=float(close.pct_change().tail(20).std()*math.sqrt(252)*100)
                if not all(map(math.isfinite,[momentum,trend,vol,liquidity])):continue
                if momentum<=0 or trend<=0 or vol>90:continue
                score=momentum+0.3*trend-0.04*vol
                candidates.append({"ticker":ticker,"price":round(price,2),"momentum_5d_pct":round(momentum,2),"volatility_20d_pct":round(vol,2),"score":score,"as_of":str(date.date()),"rationale":"Positive 5- and 20-session price momentum; passed minimum liquidity and volatility filters. This is a screening observation, not a forecast."})
            except Exception as exc:
                print(f"Skip {ticker}: {type(exc).__name__}: {exc}")
        if len(candidates)>=5:
            candidates.sort(key=lambda c:c["score"],reverse=True)
            picks=candidates[:5]
            result.update(status="ok",price_as_of=min(p["as_of"] for p in picks),picks=[{**{k:v for k,v in p.items() if k not in ("score","as_of")},"rank":i} for i,p in enumerate(picks,1)],message="Experimental ranking, not independently validated.")
        else: result["message"]=f"Only {len(candidates)} candidates passed screening; fewer than five. No ranking published."
    except Exception as exc:result["message"]=f"Scan failed: {type(exc).__name__}"
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    print(result["status"],result["message"])
if __name__=="__main__":main()
