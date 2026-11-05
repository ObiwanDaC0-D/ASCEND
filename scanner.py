"""ASCEND V5: benchmark-aware research with time-ordered holdout and an exploratory alternative-data lab.
Not a trading recommendation, probability model, or verified predictive edge.
"""
import json, math, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import numpy as np
import pandas as pd
import requests
import yfinance as yf
import xml.etree.ElementTree as ET
from institutional import fetch_insider_context
from alternative_lab import evaluate as evaluate_alternative

TICKERS="AAPL MSFT NVDA AMZN GOOGL META AVGO AMD TSM COST JPM V MA UNH LLY XOM CAT GE ORCL NFLX CRM ADBE QCOM TXN AMAT MU UBER PANW NOW WMT HD BAC ABBV KO PEP IBM CSCO INTU PLTR ANET".split()
OUT=Path("data/latest.json")
POS={"beats","beat","surges","growth","record","raises","upgrade","expands","approval","wins","profit","strong"}
NEG={"misses","miss","cuts","downgrade","lawsuit","probe","falls","decline","recall","warning","loss","weak"}
def news(ticker):
    try:
        url="https://news.google.com/rss/search?q="+quote(ticker+" stock when:2d")+"&hl=en-US&gl=US&ceid=US:en"
        r=requests.get(url,timeout=8,headers={"User-Agent":"ASCEND/3.0 educational research"});r.raise_for_status()
        titles=list(dict.fromkeys(n.text or "" for n in ET.fromstring(r.content).findall("./channel/item/title")))[:12]
        tokens=[set("".join(c.lower() if c.isalpha() else " " for c in s).split()) for s in titles]
        return {"status":"context_only","count":len(titles),"lexicon_balance":sum(len(t&POS)-len(t&NEG) for t in tokens),"headlines":titles[:3]}
    except Exception:return {"status":"unavailable","count":0,"lexicon_balance":None,"headlines":[]}
def frame(ticker):
    df=yf.download(ticker,period="3y",interval="1d",auto_adjust=True,progress=False,threads=False)
    if df.empty:return None
    c=df["Close"].squeeze().dropna().astype(float)
    v=df["Volume"].squeeze().reindex(c.index).astype(float)
    if len(c)<300:return None
    return c,v
def diagnostics(c,bench):
    """Past-only signals and strictly subsequent five-session outcomes.
    Holdout is the latest 120 eligible sessions with a five-session embargo.
    Overlapping forward returns remain dependent; results are descriptive.
    """
    b=bench.reindex(c.index).ffill()
    if b.isna().sum()>10:return None
    features=pd.DataFrame(index=c.index)
    features["mom5"]=c.pct_change(5)
    features["mom20"]=c.pct_change(20)
    features["vol"]=c.pct_change().rolling(20).std()*np.sqrt(252)
    features["forward"]=c.shift(-5)/c-1
    features["bench_forward"]=b.shift(-5)/b-1
    features=features.iloc[:-5].dropna()
    if len(features)<200:return None
    train=features.iloc[:-120]
    holdout=features.iloc[-120:]
    def evaluate(x):
        s=x[(x.mom5>0)&(x.mom20>0)&(x.vol<.9)]
        if len(s)<8:return None
        active=s.forward-s.bench_forward
        return {"signals":len(s),"positive_fraction":round(float((s.forward>0).mean()),3),"average_return_pct":round(float(s.forward.mean()*100),2),"average_excess_vs_spy_pct":round(float(active.mean()*100),2)}
    a=evaluate(train);b=evaluate(holdout)
    if not a or not b:return None
    return {"training":a,"holdout":b,"holdout_sessions":120,"method":"time-ordered historical holdout, overlapping 5-session forward returns; descriptive, not statistically independent"}
def main():
    now=datetime.now(timezone.utc)
    out={"version":5,"status":"unavailable","generated_at":now.isoformat(),"price_as_of":None,"universe_size":len(TICKERS),"method":"price momentum, liquidity, volatility; time-ordered holdout vs SPY","picks":[],"message":"No qualified opportunities.","alternative_lab":{"status":"research_only","message":"Unconventional relationships are not allowed to affect rankings without pre-registered, out-of-sample validation."},"warnings":["Experimental heuristic, not a calibrated return forecast.","Overlapping outcomes and selection effects limit inference.","News and alternative signals do not influence rankings."]}
    try:
        spy=frame("SPY")
        if spy is None:raise RuntimeError("Benchmark data unavailable")
        bench=spy[0]
        candidates=[]
        for ticker in TICKERS:
            try:
                item=frame(ticker)
                if item is None:continue
                c,v=item
                stamp=pd.Timestamp(c.index[-1]);stamp=stamp.tz_localize("UTC") if stamp.tzinfo is None else stamp.tz_convert("UTC")
                if (now-stamp.to_pydatetime()).days>5:continue
                price=float(c.iloc[-1]);liquidity=float((c.tail(20)*v.tail(20)).mean())
                mom=float((price/c.iloc[-6]-1)*100);trend=float((price/c.iloc[-21]-1)*100)
                vol=float(c.pct_change().tail(20).std()*np.sqrt(252)*100)
                if not all(math.isfinite(x) for x in [price,liquidity,mom,trend,vol]):continue
                if price<5 or liquidity<20_000_000 or mom<=0 or trend<=0 or vol>=90:continue
                diag=diagnostics(c,bench)
                if not diag:continue
                # Holdout is reported but deliberately NOT used to optimize ranking.
                score=mom+.3*trend-.04*vol
                candidates.append({"ticker":ticker,"price":round(price,2),"momentum_5d_pct":round(mom,2),"trend_20d_pct":round(trend,2),"volatility_20d_pct":round(vol,2),"liquidity_usd":round(liquidity),"validation":diag,"score":score,"as_of":stamp.date().isoformat(),"rationale":"Qualified price trend and liquidity filters; historical holdout evidence is descriptive and may not generalize."})
            except Exception as exc:print("skip",ticker,type(exc).__name__,str(exc)[:90])
        candidates.sort(key=lambda x:x["score"],reverse=True)
        if len(candidates)>=5:
            picks=candidates[:5]
            for i,p in enumerate(picks,1):
                p.pop("score");p["rank"]=i;p["news"]=news(p["ticker"]);time.sleep(.15)
            out["institutional"]=fetch_insider_context([p["ticker"] for p in picks])
            try:
                nvda=frame("NVDA")
                out["alternative_lab"]=evaluate_alternative(nvda[0]) if nvda is not None else {"status":"unavailable"}
            except Exception as exc:
                out["alternative_lab"]={"status":"unavailable","reason":type(exc).__name__}
            for p in picks:
                p["institutional"]=out["institutional"].get("companies",{}).get(p["ticker"],{})
            out.update(status="ok",picks=picks,price_as_of=min(p["as_of"] for p in picks),message="Five experimental screening candidates; predictive advantage not established.")
        else:out["message"]=f"Only {len(candidates)} qualified candidates; no five-stock list published."
    except Exception as exc:out["message"]="Scan unavailable: "+type(exc).__name__+" "+str(exc)[:100]
    try:
        from journal import update as update_journal
        out["performance"]=update_journal(out)
    except Exception as exc:
        out["performance"]={"status":"unavailable","reason":type(exc).__name__}
        print("journal unavailable:",type(exc).__name__,str(exc)[:100])
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(out["status"],out["message"])
if __name__=="__main__":main()
