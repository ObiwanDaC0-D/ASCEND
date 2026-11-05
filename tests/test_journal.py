import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import journal
class JournalTests(unittest.TestCase):
    def test_deduplicates_same_session_and_waits_for_future(self):
        idx=pd.date_range("2026-10-01",periods=9,freq="B")
        c=pd.Series([100,101,102,103,104,105,106,107,108],index=idx)
        snapshot={"status":"ok","price_as_of":idx[-1].date().isoformat(),"picks":[{"ticker":t,"rank":i+1} for i,t in enumerate(["HD","MA","LLY","WMT","V"])]}
        with tempfile.TemporaryDirectory() as d,patch.object(journal,"PATH",Path(d)/"performance.json"),patch.object(journal,"series",return_value=c):
            a=journal.update(snapshot);b=journal.update(snapshot)
            self.assertEqual(a["signal_days"],1)
            self.assertEqual(b["signal_days"],1)
            self.assertEqual(b["summary"]["2"]["observations"],0)
    def test_records_only_matured_outcomes(self):
        idx=pd.date_range("2026-10-01",periods=10,freq="B")
        c=pd.Series([100+i for i in range(10)],index=idx,dtype=float)
        snapshot={"status":"ok","price_as_of":idx[4].date().isoformat(),"picks":[{"ticker":t,"rank":i+1} for i,t in enumerate(["HD","MA","LLY","WMT","V"])]}
        with tempfile.TemporaryDirectory() as d,patch.object(journal,"PATH",Path(d)/"performance.json"),patch.object(journal,"series",return_value=c):
            journal.update(snapshot);result=journal.update({"status":"unavailable"})
            self.assertEqual(result["summary"]["2"]["observations"],5)
            self.assertEqual(result["summary"]["5"]["observations"],0)
if __name__=="__main__":unittest.main()
