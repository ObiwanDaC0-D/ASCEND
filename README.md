# ASCEND — The Five v3.0

Minimal one-button GitHub Pages research interface, with scheduled Python scanning.

## Activation
1. **Settings → Pages → Deploy from a branch → main / (root)**.
2. **Actions → ASCEND daily market scan → Run workflow** to produce a V3 scan.
3. Open the published page and press **LAUNCH ASCEND**.

## V3 additions
- Time-ordered historical holdout: last 120 eligible sessions, earlier sessions as training period.
- SPY-relative 5-session forward returns and positive-outcome frequency.
- Benchmark-aware diagnostics shown in expandable research details.
- Fail-closed version check, preventing old V2 data from masquerading as V3 results.
- Explicit alternative-data research gate: unconventional correlations remain excluded from rankings until independently validated.
- Existing contextual news headlines, liquidity and momentum filters retained.

## Important limits
This is **not** a predictive intelligence model with demonstrated edge. The ranking is still a simple momentum heuristic; historical results are overlapping and subject to dependence and selection bias. The holdout is descriptive and **not used for optimizing the score**, but the universe and strategy design are not pre-registered. No SEC ownership ingestion, weather/quantum data feed, real-time job trigger, calibrated confidence, portfolio risk sizing, or broker execution is implemented. News remains context only. Market data from yfinance may fail or be delayed.

GitHub Actions runs on weekdays at 22:30 UTC, subject to delays. The Launch button reads the last published JSON rather than starting a remote job.
