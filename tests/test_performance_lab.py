import unittest
from performance_lab import summarize
class PerformanceLabTests(unittest.TestCase):
    def test_requires_complete_five_stock_cohort(self):
        records=[{"signal_date":"2026-11-04","picks":[{"outcomes":{"2":{"net_pct":2,"spy_pct":1,"excess_net_pct":1}}} for _ in range(4)]}]
        self.assertEqual(summarize(records,2)["completed_cohorts"],0)
    def test_equal_weighted_cohort(self):
        records=[{"signal_date":"2026-11-04","picks":[{"outcomes":{"2":{"net_pct":x,"spy_pct":1,"excess_net_pct":x-1}}} for x in [1,2,3,4,5]]}]
        s=summarize(records,2)
        self.assertEqual(s["completed_cohorts"],1)
        self.assertEqual(s["average_basket_net_pct"],3)
        self.assertEqual(s["average_basket_excess_pct"],2)
        self.assertIsNone(s["uncertainty_95_pct"])
if __name__=="__main__":unittest.main()
