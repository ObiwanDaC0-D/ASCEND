# ASCEND — The Five v2.0

Minimal GitHub Pages interface with a scheduled, experimental market research pipeline.

## Start
1. **Settings → Pages → Deploy from a branch → main / (root)**.
2. **Actions → ASCEND daily market scan → Run workflow**.
3. Open the published page and press **LAUNCH ASCEND** to read the latest published scan.

## What's new in V2
- Expanded watch universe (38 liquid U.S.-listed stocks, not the entire market).
- Historical 5-session forward-return diagnostics computed using only past data for features.
- A minimum of 12 qualifying historical observations per candidate.
- Recent Google News RSS headlines collected as **context only**, never fed into trading scores.
- Improved candidate details, last-update timestamp and staleness warning.
- Fail-closed results when data is missing or fewer than five qualify.

## Scientific caveats
The scoring formula remains an **unvalidated momentum heuristic**. Historical observations overlap, and the exploratory positive-return fraction is **not a calibrated prediction**. No cross-sectional benchmark, risk-adjusted expected-return forecast, formal multiple-testing correction, real-time feed, broker integration, or institutional/quantum correlation engine is implemented yet. News RSS may be blocked or incomplete. Yahoo Finance via yfinance is not a guaranteed or licensed production market-data service. Results may lag market hours or fail entirely. No trades are placed.

## Next milestones
Point-in-time event archives, genuine walk-forward strategy-vs-benchmark evaluation, confidence intervals, institutional filings, controlled alternative-data experiments, and an authenticated job-trigger endpoint (the current button loads the latest scheduled result).
