#!/usr/bin/env python3
"""Analyze a normalized, source-attributed FDA/EMA oncology approval CSV."""
import argparse,csv,json,statistics
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.request import Request,urlopen

FIELDS=("agency","medicine","application_date","approval_date","pathway","source_url")
def fetch_openfda(url,limit=100):
 req=Request(url+ ("&" if "?" in url else "?")+f"limit={limit}",headers={"User-Agent":"regulatory-analytics-reconstruction/1.0"})
 with urlopen(req,timeout=20) as r:return json.load(r)
def analyze(rows):
 groups=defaultdict(list); invalid=[]
 for i,r in enumerate(rows,1):
  try:
   if r["agency"] not in {"FDA","EMA"}:raise ValueError("agency must be FDA or EMA")
   lag=(date.fromisoformat(r["approval_date"])-date.fromisoformat(r["application_date"])).days
   if lag<0:raise ValueError("approval precedes application")
   groups[(r["agency"],r.get("pathway") or "unspecified")].append(lag)
  except (KeyError,ValueError) as e:invalid.append({"row":i,"reason":str(e)})
 summary=[{"agency":a,"pathway":p,"n":len(xs),"mean_lag_days":round(statistics.mean(xs),1),"median_lag_days":statistics.median(xs)} for (a,p),xs in sorted(groups.items())]
 return {"groups":summary,"invalid_rows":invalid,"limitations":"Descriptive sample statistics only; source coverage and pathway definitions must be checked before comparing agencies."}
def main():
 p=argparse.ArgumentParser();p.add_argument("input",type=Path,help="normalized CSV with fields: "+", ".join(FIELDS));p.add_argument("--output",type=Path,default=Path("summary.json"));a=p.parse_args()
 with a.input.open(newline="",encoding="utf-8-sig") as f: result=analyze(list(csv.DictReader(f)))
 a.output.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
if __name__=="__main__":main()
