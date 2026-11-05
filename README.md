# ASCEND 7.0 — The Five + Portfolio Research

A minimalist GitHub Pages stock research prototype. **LAUNCH ASCEND** loads the last completed scheduled scan; it does not execute live trading or trigger an immediate scan.

## Version 7\n- New collapsible five-stock basket research view with recent completed cohort history and SPY-relative comparisons.\n- Exploratory uncertainty intervals appear after 20 complete signal-day baskets.\n- Journal price retrieval extended to two years for longer tracking continuity; external data still has revision and availability limits.\n- These are descriptive paper outcomes, not a compounded or executable portfolio.\n\n## What's new
- `journal.py` records the five research candidates once per **market signal date** in `data/performance.json`.
- Subsequent scans evaluate **2-session and 5-session** outcomes only after future data is available.
- The entry proxy is the **next common trading session's adjusted closing price**, rather than the signal-day closing price. This is a hypothetical observation, **not an executable fill**.
- Measures gross returns, illustrative net returns after **10 basis points (0.10%) round-trip friction**, and SPY-relative excess returns.
- Preserves V4 momentum screening, historical holdout, SEC Form 4 context, news and alternative-data research.
- Adds a collapsed Performance Laboratory section to the otherwise unchanged one-button UI.
- Unit tests cover session deduplication and waiting for future observations.

## Activate
1. Ensure **Settings → Pages → Deploy from branch → main / (root)** is enabled.
2. In **Actions → ASCEND daily market scan**, run the workflow once. It will publish `data/latest.json` and `data/performance.json`.
3. Open the site and click **LAUNCH ASCEND**.
4. Performance metrics will initially be empty. They populate **only after future market sessions and subsequent scans**.

For optional SEC context, set the repository Actions secret `SEC_USER_AGENT` to an identifying app name and valid contact email. This secret is not published.

## Critical methodology limitations
- This is **prospective paper research**, not a brokerage simulation with executable opening fills, order books, borrow costs, spreads, taxes or slippage estimates. The next-day close can be impossible to achieve at the assumed price in practice.
- Adjusted closes can be retrospectively revised for corporate actions. Historical Yahoo Finance data may be delayed, incomplete or adjusted.
- The journal begins with **new V5 signals**; it does not pretend V4 historical picks were prospectively logged.
- A 2-session or 5-session horizon starts at the next-session hypothetical close, so the 5-session outcome requires six subsequent closing observations.
- Multiple stocks from the same day are correlated; outcomes can overlap; the displayed averages do not establish significance, causality or a reliable trading advantage.
- The current ranking remains an **unvalidated momentum heuristic**, not a calibrated probability or financial recommendation.
- No actual trading, position sizing, portfolio equity curve or portfolio-level return is calculated.
- SEC Form 4 filing counts are not purchase counts; alternative correlations are exploratory only and excluded from rankings.

## Future work
Robust timestamped signal audit trail, independent benchmark-matched portfolio accounting, realistic entry/exit execution assumptions, and uncertainty intervals. No production trading until a genuine prospective evaluation shows a defensible advantage.
