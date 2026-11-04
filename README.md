# ASCEND — The Five v4.0

A minimalist one-button research UI with scheduled Python analysis. The button loads the **last completed** scan; it does **not** start a new remote job.

## Activate
1. **Settings → Pages → Deploy from a branch → main / (root)**.
2. **Actions → ASCEND daily market scan → Run workflow**.
3. Open the Pages site and press **LAUNCH ASCEND**.

## V4 modules
- **Core screening:** experimental price momentum, liquidity, volatility ranking from a limited stock universe.
- **Historical validation:** descriptive time-ordered holdout results and excess five-session returns versus SPY; overlapping outcomes and selection bias mean these are **not calibrated forecasts**.
- **Institutional intelligence:** SEC EDGAR submissions API, counting recent Form 4 filings for selected tickers. Counts **do not establish purchases, insider sentiment, or intent**. SEC requires an identifying user agent. Configure repository **Settings → Secrets and variables → Actions → New repository secret** named `SEC_USER_AGENT`, containing an app name and a real contact email (for example, `ASCEND Research your-email@domain.com`). Do not put personal email in source code. Missing secret disables this feature without failing the scan.
- **Serendipity lab:** exploratory NVDA daily-return vs San Diego temperature correlations at 1–5 calendar-day lags using Open-Meteo historical weather; a 500-iteration circular-shift max-lag permutation comparison. **No holdout, seasonality adjustment, causal evidence, or quantum entanglement claim**. Excluded from stock rankings.
- **News:** contextual RSS headlines; excluded from scores.
- **Tests:** GitHub Actions runs basic research tests before the scanner.

## Data quality and limitations
Yahoo Finance/yfinance and public feeds can be delayed, rate-limited, incomplete or unavailable. Research may show no results. The stock ranking is a heuristic, **not a proven predictive edge** or personalized investment advice. The holdout is not an independent prospective validation of the overall research process. SEC filing counts and temperature correlations are exploratory context only. No broker execution, portfolio allocation, or authenticated on-demand scan exists.

## Next
Validate against a pre-registered prospective paper-trading record, implement robust historical event archives, correct for multiple hypothesis search, and build a secure on-demand backend before treating the system as investment-grade.
