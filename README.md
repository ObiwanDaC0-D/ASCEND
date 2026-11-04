# ASCEND — The Five (v1.0)

A minimalist GitHub Pages-compatible **market research prototype**. Click **LAUNCH ASCEND** to view up to five candidates from the latest completed scan.

## Setup
1. In GitHub **Settings → Pages**, select **Deploy from a branch**, **main**, **/(root)**.
2. Open **Actions → ASCEND daily market scan → Run workflow** to produce the first dataset.
3. Return to the Pages URL and click **LAUNCH ASCEND**.

## How it works
The scheduled workflow runs on weekdays at 22:30 UTC (GitHub schedules can be delayed). Python requests daily adjusted stock prices for a starter 30-stock universe, filters for liquidity, 5-day and 20-day positive momentum and annualized volatility, then ranks up to five candidates. The frontend reads `data/latest.json`. The launch button loads the latest scan; it **does not initiate a new server-side job**. If fewer than five candidates qualify, or data retrieval fails, no picks are published.

## Limitations and next steps
This is **not a validated prediction system**. The score is an experimental heuristic, not a probability of success or a personalized buy recommendation. Prices are last daily closes, not live quotes. Yahoo Finance/yfinance may be delayed, restricted, or rate-limited; verify licensing before production use. No broker integration or automatic trading is implemented.

Later versions: point-in-time news and SEC data, institutional intelligence, alternative-data correlation research, statistical falsification, walk-forward validation, paper trading, benchmark comparisons, and risk-aware portfolio recommendations.
