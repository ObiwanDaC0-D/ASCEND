"""ASCEND V8: descriptive downside and cost-sensitivity diagnostics.

No brokerage simulation. Overlapping cohorts are excluded from the sequential
illustration; reported drawdown is NOT the drawdown of a tradable portfolio.
"""
from statistics import mean

def evaluate(records, horizon, round_trip_bps=(5,10,25,50)):
    groups=[]
    for r in sorted(records,key=lambda x:x.get("signal_date","")):
        picks=r.get("picks",[])
        if len(picks)!=5:continue
        values=[p.get("outcomes",{}).get(str(horizon)) for p in picks]
        if any(v is None for v in values):continue
        entries=[p.get("entry_date") for p in picks]
        exits=[v.get("exit_date") for v in values]
        if not all(entries) or not all(exits):continue
        gross=mean(float(v["gross_pct"]) for v in values)
        spy=mean(float(v["spy_pct"]) for v in values)
        groups.append({"signal_date":r["signal_date"],"entry_date":max(entries),
                       "exit_date":max(exits),"gross_pct":gross,"spy_pct":spy})
    output={"completed_cohorts":len(groups),"negative_fraction":None,"worst_net_pct":None,
            "cost_sensitivity":[],"sequential_illustration":{"cohorts":0,"total_return_pct":None,"max_drawdown_pct":None,"spy_total_return_pct":None},
            "note":"Cost assumptions are hypothetical. Sequential illustration skips overlapping cohorts and compounds selected completed baskets; not an executable portfolio or unbiased backtest."}
    if not groups:return output
    # Use the original journal's 10 bps convention as the base case.
    net=[g["gross_pct"]-.10 for g in groups]
    output["negative_fraction"]=round(sum(x<0 for x in net)/len(net),3)
    output["worst_net_pct"]=round(min(net),3)
    output["cost_sensitivity"]=[{"round_trip_bps":bps,"mean_basket_net_pct":round(mean(g["gross_pct"]-bps/100 for g in groups),3),
                                  "mean_excess_vs_spy_pct":round(mean(g["gross_pct"]-bps/100-g["spy_pct"] for g in groups),3)} for bps in round_trip_bps]
    # Avoid counting capital in overlapping baskets. A basket may be skipped even
    # though it would have been selected live. The sequence is diagnostic only.
    selected=[];last_exit=""
    for g in groups:
        if g["entry_date"]<=last_exit:continue
        selected.append(g);last_exit=g["exit_date"]
    wealth=1.;benchmark=1.;peak=1.;drawdown=0.
    for g in selected:
        wealth*=1+(g["gross_pct"]-.10)/100
        benchmark*=1+g["spy_pct"]/100
        peak=max(peak,wealth)
        drawdown=max(drawdown,100*(1-wealth/peak))
    output["sequential_illustration"]={"cohorts":len(selected),"total_return_pct":round((wealth-1)*100,3),
                                        "max_drawdown_pct":round(drawdown,3),
                                        "spy_total_return_pct":round((benchmark-1)*100,3)}
    return output
