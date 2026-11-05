import unittest
from risk_lab import evaluate
def cohort(date,entry,exit,gross,spy=0):
    return {"signal_date":date,"picks":[{"ticker":str(i),"entry_date":entry,
            "outcomes":{"2":{"gross_pct":gross,"spy_pct":spy,"exit_date":exit}}} for i in range(5)]}
class RiskLabTests(unittest.TestCase):
    def test_no_matured_data(self):
        self.assertEqual(evaluate([],2)["completed_cohorts"],0)
    def test_cost_sensitivity(self):
        a=evaluate([cohort("2026-11-01","2026-11-02","2026-11-04",2,1)],2)
        self.assertEqual(a["cost_sensitivity"][1]["mean_basket_net_pct"],1.9)
        self.assertEqual(a["cost_sensitivity"][1]["mean_excess_vs_spy_pct"],.9)
    def test_skips_overlap_in_sequence(self):
        a=evaluate([cohort("2026-11-01","2026-11-02","2026-11-04",-10),
                    cohort("2026-11-02","2026-11-03","2026-11-05",20),
                    cohort("2026-11-05","2026-11-06","2026-11-10",5)],2)
        self.assertEqual(a["completed_cohorts"],3)
        self.assertEqual(a["sequential_illustration"]["cohorts"],2)
        self.assertGreater(a["sequential_illustration"]["max_drawdown_pct"],0)
if __name__=="__main__":unittest.main()
