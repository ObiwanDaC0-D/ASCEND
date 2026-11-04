"""Pre-registered illustrative alternative-data test: NVDA vs San Diego daily temperature.
Max-lag permutation adjusts for searching lags; exploratory only, never used in stock scores.
"""
import numpy as np, pandas as pd, requests
from datetime import timedelta
def evaluate(nvda):
    try:
        end=pd.Timestamp(nvda.index[-1]).date()
        start=max(pd.Timestamp(nvda.index[0]).date(),end-timedelta(days=365))
        url="https://archive-api.open-meteo.com/v1/archive"
        params={"latitude":32.7157,"longitude":-117.1611,"start_date":start.isoformat(),"end_date":end.isoformat(),"daily":"temperature_2m_mean","timezone":"America/Los_Angeles"}
        r=requests.get(url,params=params,timeout=18);r.raise_for_status()
        d=r.json()["daily"];weather=pd.Series(d["temperature_2m_mean"],index=pd.to_datetime(d["time"]),dtype=float)
        stock=nvda.copy();stock.index=pd.to_datetime(stock.index).tz_localize(None).normalize()
        returns=stock.pct_change().rename("return")
        # Only prior calendar-day temperature may predict a subsequent stock session.
        # Evaluate fixed lead windows 1, 2, 3, 4, 5 days; guard against searching lags.
        common=pd.DataFrame({"return":returns})
        for lag in range(1,6):
            # On stock date t, only use weather dated t-lag.
            common[f"temp_lag_{lag}"]=weather.reindex(common.index-pd.Timedelta(days=lag)).to_numpy()
        common=common.dropna()
        if len(common)<100:return {"status":"insufficient_data","observations":len(common)}
        x=common[[f"temp_lag_{i}" for i in range(1,6)]].to_numpy()
        y=common["return"].to_numpy()
        x=(x-x.mean(axis=0))/x.std(axis=0)
        y=(y-y.mean())/y.std()
        corr=(x*y[:,None]).mean(axis=0)
        observed=float(np.max(np.abs(corr)))
        # Circular shifts preserve autocorrelation within each series more than random shuffling.
        rng=np.random.default_rng(20261104);null=[]
        for _ in range(500):
            shift=int(rng.integers(15,len(y)-15))
            yy=np.roll(y,shift)
            null.append(float(np.max(np.abs((x*yy[:,None]).mean(axis=0)))))
        p=(1+sum(z>=observed for z in null))/(len(null)+1)
        return {"status":"exploratory_only","target":"NVDA daily returns","predictor":"San Diego daily mean temperature","observations":len(common),"lag_days":int(np.argmax(np.abs(corr))+1),"correlation":round(float(corr[np.argmax(np.abs(corr))]),4),"max_lag_permutation_p":round(p,4),"permutations":500,"warning":"Illustrative exploratory test; no independent holdout, seasonality controls, or causal evidence. Not quantum entanglement and not used in rankings."}
    except Exception as exc:return {"status":"unavailable","reason":type(exc).__name__}
