"""ASCEND V10 market data quality checks."""
import pandas as pd

def coherent_sessions(picks,price_as_of):
    return len(picks)==5 and len({p['ticker'] for p in picks})==5 and all(p.get('as_of')==price_as_of for p in picks)

def valid_history(series):
    if series is None or len(series)<30:return False
    index=pd.to_datetime(series.index)
    return index.is_monotonic_increasing and not index.has_duplicates and series.notna().all() and (series>0).all()
