# ASCEND 9.0 — Prospective Audit & Daily Paper Marks

ASCEND is an experimental stock research tool with a one-button GitHub Pages interface. It is **not** an investment adviser, a broker, or a validated predictive model.

## What's new in V9
- **Strategy audit metadata:** each newly recorded signal day captures the strategy identifier, a SHA-256-derived fingerprint of the documented screening rules, UTC scan timestamp, and the market data session date. Legacy entries are explicitly unversioned rather than retroactively attributed to V9.
- **Daily paper marks:** independently track the hypothetical equal-weight performance of each recorded five-stock cohort using next-session adjusted closing prices, including SPY-relative returns and a 10-basis-point illustrative round-trip cost.
- **No future-data substitution:** marks appear only for sessions already present in downloaded historical data; incomplete horizons are labeled as maturing.
- **Dashboard:** expanded Portfolio Research shows the most recent daily cohort marks and their strategy version, alongside V8 downside, costs and drawdown diagnostics.
- **Tests:** deterministic rule fingerprint and no-future-observation tests.

## Start V9
Run **Actions → ASCEND daily market scan → Run workflow** on `main`. Wait for the run to succeed, then visit the Pages site and click **LAUNCH ASCEND**. The button reads the last published scan, not an immediate new computation.

## Important limitations
- A rules fingerprint is a documentation and change-detection aid, **not an immutable or cryptographically signed audit trail**. Repository administrators can edit history or records.
- The timestamp records when the scanner generated its JSON, not the precise time the ranking decision became available at a tradeable exchange price. Earlier V5–V8 signals cannot be assumed to have V9 provenance.
- Daily marks are **per-cohort hypothetical liquidation observations**; they are not a consolidated portfolio with simultaneous position sizing, cash constraints, daily financing, turnover or trade execution.
- Next-session adjusted closes are not guaranteed executable fills. Yahoo Finance data can be delayed or retrospectively adjusted.
- Cohort outcomes overlap; the statistical interval, sequential drawdown illustration and averages are descriptive only.
- The momentum score is unvalidated. Institutional filings and unusual correlations are research context, **not** ranking inputs.

## Next priority
A fully prospective append-only external audit, an explicit time-of-signal data cutoff, real daily capital and position accounting, and independently measured executable slippage. Do not infer a profitable trading advantage from the current prototype.

## Version 10 reliability work

Data freshness and coherent trading-session checks are required before publishing a new signal.
