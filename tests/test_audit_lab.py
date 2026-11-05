import unittest
import pandas as pd
from audit_lab import record_metadata,daily_marks,RULE_HASH
class AuditTests(unittest.TestCase):
    def test_deterministic_rules(self):
        a=record_metadata({"generated_at":"2026-11-04T23:00:00+00:00","price_as_of":"2026-11-04"})
        self.assertEqual(a["rules_hash"],RULE_HASH)
        self.assertTrue(a["decision_timestamp_utc"])
    def test_marks_only_available_future(self):
        dates=pd.date_range("2026-11-04",periods=4,freq="B")
        prices={t:pd.Series([100,101,102,103],index=dates) for t in ["A","B","C","D","E","SPY"]}
        r=[{"signal_date":"2026-11-04","picks":[{"ticker":t} for t in ["A","B","C","D","E"]]}]
        result=daily_marks(r,prices,5)
        self.assertEqual(len(result["paths"][0]["marks"]),3)
        self.assertFalse(result["paths"][0]["complete"])
        self.assertEqual(result["paths"][0]["marks"][0]["basket_net_pct"],-.1)
if __name__=="__main__":unittest.main()
