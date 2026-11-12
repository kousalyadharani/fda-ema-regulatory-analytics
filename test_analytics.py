import unittest
from analytics import analyze
class AnalyticsTests(unittest.TestCase):
 def test_agency_and_pathway_lag_summary(self):
  r=analyze([{"agency":"FDA","application_date":"2020-01-01","approval_date":"2020-01-11","pathway":"standard"}]);self.assertEqual(r["groups"][0]["mean_lag_days"],10)
 def test_bad_date_is_reported(self): self.assertEqual(len(analyze([{"agency":"EMA"}])["invalid_rows"]),1)
if __name__=="__main__":unittest.main()
