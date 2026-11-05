# ASCEND 8.0 — Portfolio Risk Laboratory

ASCEND is an experimental, one-button market research application. It does not place orders or claim a demonstrated predictive edge.

## Version 8
- New `risk_lab.py` reports downside frequency and the worst completed equal-weight five-stock basket at each 2- and 5-session evaluation horizon.
- Compares **5, 10, 25, and 50 basis points** of hypothetical round-trip trading friction.
- Adds a **non-overlapping sequential illustration**: chooses completed baskets chronologically, skipping baskets whose hypothetical entry overlaps a prior basket's exit. Shows compounded returns, matched SPY comparison and observed maximum drawdown.
- Displays risk metrics in the collapsible Portfolio Research panel while keeping the single Launch button.
- Includes unit tests for cost assumptions, overlap avoidance, and empty histories.
- Retains SEC Form 4 contextual filing counts, SPY-relative historical diagnostics, alternative-data research and the prospective signal journal.

## Activate
Open **Actions → ASCEND daily market scan → Run workflow**. Wait for a successful run, then open GitHub Pages and click **LAUNCH ASCEND**. The button loads the last published scan, not an immediate live scan. Performance statistics may remain empty until enough future market sessions have passed.

## Interpretation and safeguards
- Entries are **next-session adjusted closing prices**, not guaranteed tradeable fills. Historical adjustments may change.
- The cost model is a sensitivity analysis, not observed spreads, market impact, commissions, taxes or borrow costs.
- The sequential illustration **does not model live capital allocation, cash, simultaneous positions, orders, or changing exposures**. Skipping overlapping baskets creates a selective research path, not a validated strategy.
- The displayed maximum drawdown applies **only to the hypothetical sequential cohort path** and may severely understate real intraperiod drawdowns.
- Cohort results may be correlated and selected under a changing research process. Bootstrap intervals are descriptive and not proof of an edge.
- The screening formula is still an unvalidated momentum heuristic. No real-money execution is supported.

## Next validation priorities
Independent prospective paper trading with executable timestamped price assumptions, daily mark-to-market equity accounting, transaction-cost measurements, versioned strategy rules, and a genuinely untouched evaluation period.
