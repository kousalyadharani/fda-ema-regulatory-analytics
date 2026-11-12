# FDA & EMA Regulatory Approval Analytics

Reconstructed from the portfolio's description of automated openFDA collection, web-sourced regulatory data, analysis of 200+ oncology approvals, and Power BI timeline views. This repo contains no original data extract, scraper output, or Power BI workbook.

## Run

Prepare a CSV with `agency,medicine,application_date,approval_date,pathway,source_url`, then run `python3 analytics.py approvals.csv`. Dates use ISO `YYYY-MM-DD`; invalid rows are listed rather than silently included. The summary reports counts and mean/median lag by agency and pathway.

The analysis requires a consistently sourced and defined FDA/EMA sample before comparing agencies. It is descriptive, not causal, and does not assert the portfolio's original sample size or reproduce its dashboard. `fetch_openfda` is a bounded standard-library API fetch helper; EMA rows require a separately sourced input.

## Verify

`python3 -m unittest -v`
