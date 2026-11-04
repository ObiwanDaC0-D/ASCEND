"""Public SEC EDGAR Form 4 activity context. No inference of insider intent."""
import os, requests
from datetime import datetime, timedelta, timezone
API="https://data.sec.gov"
def fetch_insider_context(tickers):
    agent=os.environ.get("SEC_USER_AGENT","ASCEND educational research contact research@example.org")
    if "example.org" in agent:return {"status":"not_configured","message":"Set SEC_USER_AGENT to an identifying app name and real contact email in GitHub Actions secrets.","companies":{}}
    headers={"User-Agent":agent,"Accept-Encoding":"gzip, deflate","Host":"data.sec.gov"}
    try:
        r=requests.get("https://www.sec.gov/files/company_tickers.json",headers={"User-Agent":agent},timeout=12);r.raise_for_status()
        mapping={str(x["ticker"]).upper():str(x["cik_str"]).zfill(10) for x in r.json().values()}
    except Exception as exc:return {"status":"unavailable","message":type(exc).__name__,"companies":{}}
    result={}
    cutoff=(datetime.now(timezone.utc)-timedelta(days=90)).date().isoformat()
    for ticker in tickers:
        cik=mapping.get(ticker)
        if not cik:continue
        try:
            r=requests.get(f"{API}/submissions/CIK{cik}.json",headers=headers,timeout=10);r.raise_for_status()
            recent=r.json().get("filings",{}).get("recent",{})
            filings=[{"filed":date,"accession":acc} for form,date,acc in zip(recent.get("form",[]),recent.get("filingDate",[]),recent.get("accessionNumber",[])) if form=="4" and date>=cutoff]
            result[ticker]={"form4_count_90d":len(filings),"latest_filed":filings[0]["filed"] if filings else None,"cik":cik,"note":"Form 4 filing counts are NOT insider purchases; filings can include sales, awards and other transactions."}
        except Exception:result[ticker]={"status":"unavailable"}
    return {"status":"context_only","source":"SEC EDGAR submissions","companies":result,"message":"Public disclosure filing counts; never included in ranking."}
