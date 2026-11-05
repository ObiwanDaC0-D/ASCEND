import unittest
import pandas as pd
from quality_lab import coherent_sessions,valid_history

class QualityTests(unittest.TestCase):
    def test_reject_duplicate_tickers(self):
        self.assertFalse(coherent_sessions([{'ticker':'A','as_of':'2026-11-04'}]*5,'2026-11-04'))
    def test_reject_mixed_sessions(self):
        p=[{'ticker':str(i),'as_of':'2026-11-04'} for i in range(5)]
        p[2]['as_of']='2026-11-03'
        self.assertFalse(coherent_sessions(p,'2026-11-04'))
    def test_reject_bad_history(self):
        s=pd.Series([1.,2.,0.],index=pd.date_range('2026-01-01',periods=3))
        self.assertFalse(valid_history(s))

if __name__=='__main__':unittest.main()
