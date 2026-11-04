"""ASCEND v2: point-in-time cautious market research, not investment advice."""
import json, math, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import requests
import yfinance as yf
import xml.etree.ElementTree as ET
from urllib.parse import quote

TICKERS="AAPL MSFT NVDA AMZN GOOGL META AVGO AMD TSM COST JPM V MA UNH LLY XOM CAT GE ORCL NFLX CRM ADBE QCOM TXN AMAT MU UBER PANW NOW WMT HD BAC ABBV KO PEP IBM CSCO INTU PLTR ANET".split()
OUT=Path("data/latest.json")
HEADERS={"User-Agent":"ASCENDResearch/2.0 (public educational project)"}
POS={"beats","beat","surges","growth","record","raises","upgrade","expands","approval","wins","profit","strong","rebound"}
NEG={"misses","miss","cuts","downgrade","lawsuit","probe","falls","decline","recall","warning","loss","weak","investigation"}
def finite(x): return math.isfinite(float(x))
def headline_signal(ticker):
    """News headlines are contextual only: no direct trading-score influence."""
    try:
        url="https://news.google.com/rss/search?q="+quote(ticker+" stock when:2d")+"&hl=en-US&gl=US&ceid=US:en"
        r=requests.get(url,headers=HEADERS,timeout=9);r.raise_for_status()
        root=ET.fromstring(r.content)
        titles=[n.text or "" for n in root.findall("./channel/item/title")][:15]
        unique=list(dict.fromkeys(titles))
        tokens=[set(''.join(c.lower() if c.isalpha() else ' ' for c in s).split()) for s in unique]
        sentiment=sum(len(x&POS)-len(x&NEG) for x in tokens)
        return {"count":len(unique),"lexicon_balance":sentiment,"headlines":unique[:3],"status":"context_only"}
    except Exception:
        return {"count":0,"lexicon_balance":None,"headlines":[],"status":"unavailable"}
def backtest(close):
    """Walk-forward fixed-rule signal, outcomes strictly AFTER signal date.
    Observations overlap; descriptive diagnostics, not significance or calibrated odds.
    """
    ret=close.pct_change()
    market=close.pct_change(5)
    trend=close.pct_change(20)
    vol=ret.rolling(20).std()*np.sqrt(252)
    future=close.shift(-5)/close-1
    valid=(market>0)&(trend>0)&(vol<0.9)&future.notna()
    # Restrict validation to last ~180 trading days; past-only features.
    test=valid.iloc[-185:-5]
    outcomes=future.loc[test.index][test]
    if len(outcomes)<12:return None
    wins=int((outcomes>0).sum())
    return {"historical_signals":int(len(outcomes)),"positive_5d_fraction":round(wins/len(outcomes),3),"average_5d_return_pct":round(float(outcomes.mean()*100),2),"method":"overlapping historical forward returns; exploratory only"}
def main():
    now=datetime.now(timezone.utc)
    output={"version":2,"status":"unavailable","generated_at":now.isoformat(),"price_as_of":None,"universe_size":len(TICKERS),"method":"trend, liquidity, volatility and descriptive walk-forward diagnostics","picks":[],"message":"No qualified results.","warnings":["Not a validated forecast or trading recommendation.","News is contextual and does not influence ranking."]}
    candidates=[]
    try:
        for ticker in TICKERS:
            try:
                df=yf.download(ticker,period="2y",interval="1d",auto_adjust=True,progress=False,threads=False)
                if df.empty:continue
                close=df["Close"].squeeze().dropna().astype(float)
                volume=df["Volume"].squeeze().reindex(close.index).astype(float)
                if len(close)<260:continue
                stamp=pd.Timestamp(close.index[-1])
                if stamp.tzinfo is None:stamp=stamp.tz_localize("UTC")
                if (now-stamp.to_pydatetime()).days>5:continue
                price=float(close.iloc[-1]);liquidity=float((close.tail(20)*volume.tail(20)).mean())
                mom=float((price/close.iloc[-6]-1)*100)
                trend=float((price/close.iloc[-21]-1)*100)
                volatility=float(close.pct_change().tail(20).std()*np.sqrt(252)*100)
                if not all(finite(v) for v in (price,liquidity,mom,trend,volatility)):continue
                if price<5 or liquidity<20_000_000 or mom<=0 or trend<=0 or volatility>=90:continue
                diag=backtest(close)
                if diag is None:continue
                # Descriptive ranking only. Historical hit rate is deliberately not presented as a forecast.
                score=mom+0.3*trend-0.04*volatility
                candidates.append({"ticker":ticker,"price":round(price,2),"momentum_5d_pct":round(mom,2),"trend_20d_pct":round(trend,2),"volatility_20d_pct":round(volatility,2),"liquidity_usd":round(liquidity),"backtest":diag,"score":score,"as_of":stamp.date().isoformat(),"rationale":"Positive short-term trend, liquid trading and qualifying historical observations. Historical outcomes do not guarantee future results."})
            except Exception as exc:print("skip",ticker,type(exc).__name__,str(exc)[:100])
        candidates.sort(key=lambda p:p["score"],reverse=True)
        if len(candidates)>=5:
            picks=candidates[:5]
            for i,p in enumerate(picks,1):
                p.pop("score");p["rank"]=i;p["news"]=headline_signal(p["ticker"]);time.sleep(0.2)
            output.update(status="ok",picks=picks,price_as_of=min(p["as_of"] for p in picks),message="Experimental screening only; no predictive edge established.")
        else:output["message"]=f"Only {len(candidates)} qualified candidates; refusing to fill five slots."
    except Exception as exc:output["message"]="Scan failed: "+type(exc).__name__
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(output,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(output["status"],output["message"])
if __name__=="__main__":main()
