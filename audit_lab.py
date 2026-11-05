"""V9 immutable-in-practice signal metadata and daily paper mark-to-market.
The JSON journal is mutable on GitHub; hashes detect accidental changes, not tampering.
"""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
import pandas as pd
STRATEGY="momentum-5-20-liquidity-v1"
RULES={"universe":"fixed 40-stock starter universe","min_price":5,"min_dollar_volume_20d":20000000,"min_mom5_pct":0,"min_mom20_pct":0,"max_annual_vol_pct":90,"rank":"mom5+.3*mom20-.04*annual_vol","cost_bps":10,"entry":"next common session adjusted close"}
RULE_HASH=hashlib.sha256(json.dumps(RULES,sort_keys=True,separators=(",",":")).encode()).hexdigest()[:16]
def record_metadata(snapshot):
    return {"strategy_id":STRATEGY,"rules_hash":RULE_HASH,"decision_timestamp_utc":snapshot.get("generated_at"),
            "price_as_of":snapshot.get("price_as_of"),"rules":RULES.copy(),
            "warning":"Recorded on first successful scan for a session, not a contemporaneous exchange execution timestamp."}
def daily_marks(records,prices,horizon=5):
    """Independent cohort paths; NEVER aggregate overlapping positions as one portfolio."""
    paths=[]
    spy=prices.get("SPY")
    if spy is None:return {"status":"unavailable","paths":[]}
    for r in records:
        picks=r.get("picks",[])
        if len(picks)!=5:continue
        signal=pd.Timestamp(r["signal_date"])
        aligned={}
        for p in picks:
            c=prices.get(p["ticker"])
            if c is None:break
            aligned[p["ticker"]]=c
        if len(aligned)!=5:continue
        df=pd.concat({**aligned,"SPY":spy},axis=1).dropna()
        future=df.loc[df.index>signal]
        if future.empty:continue
        # Price marks only up to horizon+1 sessions from signal.
        future=future.iloc[:horizon+1]
        entry=future.iloc[0]
        if (entry<=0).any():continue
        marks=[]
        for day,values in future.iterrows():
            gross=sum((float(values[t])/float(entry[t])-1) for t in aligned)/5
            benchmark=float(values["SPY"]/entry["SPY"]-1)
            # Round-trip cost applied on hypothetical liquidation mark.
            net=gross-.001
            marks.append({"date":day.date().isoformat(),"basket_net_pct":round(net*100,3),
                          "spy_pct":round(benchmark*100,3),"excess_pct":round((net-benchmark)*100,3)})
        paths.append({"signal_date":r["signal_date"],"strategy_id":r.get("strategy",{}).get("strategy_id","legacy-unversioned"),
                      "complete":len(marks)>horizon,"marks":marks})
    return {"status":"descriptive","paths":paths[-30:],"cohorts_with_marks":len(paths),
            "note":"Each path independently tracks a five-stock equal-weight cohort; overlaps are not consolidated into a cash-constrained account. Next-session close is hypothetical. Cost is applied to each liquidation mark."}
