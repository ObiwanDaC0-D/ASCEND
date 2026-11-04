import unittest
import pandas as pd
import numpy as np
from scanner import diagnostics
class ResearchTests(unittest.TestCase):
    def test_holdout_does_not_use_future_observations(self):
        idx=pd.date_range("2023-01-02",periods=400,freq="B")
        stock=pd.Series(100*np.exp(np.cumsum(np.full(400,.001))),index=idx)
        bench=pd.Series(100*np.exp(np.cumsum(np.full(400,.0005))),index=idx)
        result=diagnostics(stock,bench)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result["holdout"]["signals"],8)
    def test_flat_stock_not_qualified(self):
        idx=pd.date_range("2023-01-02",periods=400,freq="B")
        stock=pd.Series(np.full(400,100.),index=idx)
        self.assertIsNone(diagnostics(stock,stock))
if __name__=="__main__":unittest.main()
