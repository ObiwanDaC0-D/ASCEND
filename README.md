# ASCEND — The Five

Minimalist GitHub Pages research application. One button retrieves five experimental momentum-screened stocks from the most recent scheduled analysis.

## Simplified interface
- One fetch of `data/latest.json` per launch, instead of two competing requests.
- Five compact stock cards showing ticker, last close and 5-session momentum.
- One expandable **Why this stock?** area per selection.
- One consolidated **Research & performance** panel for prospective outcomes, risk, cost sensitivity, and paper observations.
- Mobile-friendly layout, keyboard-visible focus states, reduced-motion support, plain-text DOM construction and clear stale-data/error messages.
- Replaced legacy inline JavaScript and duplicate `performance_view.js` with `app.js`.

## Reliability maintenance
- Added missing direct dependencies: NumPy and Requests.
- Maintained V10 coherent-session and valid-history checks.
- Preserved Python scanner, journal, benchmark, SEC filing context, and alternative research.
- Ensured the scheduled publisher can create a placeholder performance JSON if the journal fails before its first successful run.

## Activate
Run **Actions → ASCEND daily market scan → Run workflow**. After it completes successfully, open the GitHub Pages site and click **LAUNCH ASCEND**. The site is static: it cannot trigger an immediate scan.

## Limitations
The screening strategy is an unvalidated heuristic, not an investment recommendation or a calibrated probability model. Prices are historical daily closes, not live or guaranteed executable fills. Cohort returns overlap; the paper journal is not a cash-constrained brokerage account. No trading is performed. The quality gate tests internal consistency but cannot verify provider correctness. A successful end-to-end GitHub Actions run should be confirmed before relying on a new snapshot.
