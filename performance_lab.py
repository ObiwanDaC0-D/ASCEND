"""ASCEND V6 cohort-level paper evaluation; no claim of independent observations."""
import math
from statistics import mean
from collections import defaultdict
import numpy as np

def summarize(records, horizon):
    """Each completed signal-day basket gets equal stock weights.
    Report cohort-level (not trade-level) uncertainty; overlapping days remain dependent.
    """
    groups=[]
    for record in records:
        picks=record.get("picks",[])
        if len(picks)!=5:continue
        outcomes=[p.get("outcomes",{}).get(str(horizon)) for p in picks]
        if any(x is None for x in outcomes):continue
        groups.append({"signal_date":record["signal_date"],"basket_net_pct":round(mean(float(x["net_pct"]) for x in outcomes),4),
                       "benchmark_pct":round(mean(float(x["spy_pct"]) for x in outcomes),4),
                       "excess_pct":round(mean(float(x["excess_net_pct"]) for x in outcomes),4)})
    result={"completed_cohorts":len(groups),"average_basket_net_pct":None,"average_basket_excess_pct":None,
            "positive_cohort_fraction":None,"uncertainty_95_pct":None,"cohorts":groups[-30:],
            "note":"Each signal-date basket is equal-weighted; baskets can overlap in time. No capital allocation or compounded equity curve."}
    if not groups:return result
    excess=np.array([g["excess_pct"] for g in groups],dtype=float)
    result.update(average_basket_net_pct=round(mean(g["basket_net_pct"] for g in groups),3),
                  average_basket_excess_pct=round(float(excess.mean()),3),
                  positive_cohort_fraction=round(mean(g["basket_net_pct"]>0 for g in groups),3))
    if len(groups)>=20:
        # Moving-block bootstrap over ordered cohort dates; descriptive interval only.
        rng=np.random.default_rng(601)
        n=len(excess);block=min(5,max(2,int(math.sqrt(n))))
        draws=[]
        for _ in range(1000):
            sampled=[]
            while len(sampled)<n:
                start=int(rng.integers(0,n))
                sampled.extend(excess[(start+np.arange(block))%n].tolist())
            draws.append(mean(sampled[:n]))
        result["uncertainty_95_pct"]=[round(float(x),3) for x in np.percentile(draws,[2.5,97.5])]
        result["note"]+=" Block-bootstrap interval is exploratory and not proof of a predictive edge."
    return result
