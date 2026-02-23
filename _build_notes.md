# v0.2.0 Release Notes - Build Notes

## KEY FACTS
- Workspace: e:\projects\products\crypto5min-polytrader
- VPS: root@65.109.240.249, container: crypto5min-polytrader, port 8602:8601
- Dashboard password: 1Bubby1!1
- Bot trades `btc-updown-5m-*` (5-minute BTC Up/Down markets)
- Polymarket fees confirmed accurate via official docs: max 1.56% at $0.50, symmetric curve. Maker rebate 20%.
- Source: https://docs.polymarket.com/polymarket-learn/trading/fees and /maker-rebates-program
- 50+ trades total: 13W/17L filled (43.3%), 17 win_unfilled, 1 loss_unfilled, remaining resolved
- Previous version: v0.1.9

## CHANGES FOR v0.2.0
1. **Trades template fix (already deployed)**: template at templates/partials/trades.html
   - `win_unfilled` now shows dimmed "W unfilled" tag with tooltip
   - `loss_unfilled` now shows dimmed "L unfilled" tag with tooltip
   - Footer legend updated to include "unfilled" explanation
   - Previously these showed as "..." (misleading as "pending")

## FILES TO UPDATE
1. Create CHANGELOG_v0.2.0.md
2. README.md - Update docs table to reference v0.2.0 changelog
3. SETUP_GUIDE.md - Version references (currently says v0.1.8 in multiple places)
4. METRICS_AND_CAVEATS.md - Add unfilled trade display info
5. SALES_COPY.md - Add ghost/unfilled trade display to features
6. tools/release_zip.ps1 - Bump version to v0.2.0
7. .env.example - Verify, may not need changes
8. Build ZIP

## POLYMARKET FEE TABLE (confirmed from official docs Feb 2026)
| Share price | Cost 100 shares | Fee    | Eff. fee |
|------------|----------------|--------|----------|
| $0.01      | $1             | $0.00  | 0.00%    |
| $0.05      | $5             | $0.003 | 0.06%    |
| $0.10      | $10            | $0.02  | 0.20%    |
| $0.15      | $15            | $0.06  | 0.41%    |
| $0.20      | $20            | $0.13  | 0.64%    |
| $0.25      | $25            | $0.22  | 0.88%    |
| $0.30      | $30            | $0.33  | 1.10%    |
| $0.35      | $35            | $0.45  | 1.29%    |
| $0.40      | $40            | $0.58  | 1.44%    |
| $0.45      | $45            | $0.69  | 1.53%    |
| $0.50      | $50            | $0.78  | 1.56%    |
| $0.55      | $55            | $0.84  | 1.53%    |
| $0.60      | $60            | $0.86  | 1.44%    |
| $0.65      | $65            | $0.84  | 1.29%    |
| $0.70      | $70            | $0.77  | 1.10%    |
| $0.75      | $75            | $0.66  | 0.88%    |
| $0.80      | $80            | $0.51  | 0.64%    |
| $0.85      | $85            | $0.35  | 0.41%    |
| $0.90      | $90            | $0.18  | 0.20%    |
| $0.95      | $95            | $0.05  | 0.06%    |
| $0.99      | $99            | $0.00  | 0.00%    |

Max fee = 1.56% at 50% probability. Fees decrease symmetrically toward extremes.
Fees rounded to 4 decimal places. Smallest charged = 0.0001 USDC.

## OFFICIAL POLYMARKET DOCS NOTES
- Polymarket calls them "15-minute crypto" markets in docs but bot trades 5-minute (`btc-updown-5m-*`)
- Both use same fee curve
- Maker rebate: 20% on 15-min crypto markets (since Jan 19, 2026)
- Sports markets (NCAAB, Serie A) got fees starting Feb 18, 2026
- Most other Polymarket markets have NO fees

## CURRENT FILE STATUS (what needs changing)
- README.md (272 lines): Docs table at line ~178 references CHANGELOG_v0.1.9.md. Need to update to v0.2.0.
- SETUP_GUIDE.md (535 lines): References "v0.1.8" at lines ~282, ~308 in section headers. Need to update.
  - Section 11 "How order execution works (v0.1.8)" - update ref
  - Fee table already correct (matches official docs)
  - Add FAQ about unfilled/ghost trades display
- METRICS_AND_CAVEATS.md (231 lines): 
  - Win Rate section at ~line 75 mentions ghost trade detection but doesn't mention new "unfilled" display
  - Fee table already correct
  - Ghost wins section at ~line 196 needs update about new display
- SALES_COPY.md (120 lines): Mostly fine, add ghost trade display feature
- .env.example (231 lines): Fine, no changes needed
- release_zip.ps1: Line 3 has Version = "v0.1.9" - bump to v0.2.0
  - Also excludeFiles list needs to include any old changelogs? No, they ship all changelogs.

## CHANGELOG v0.2.0 CONTENT
Main changes:
1. Ghost/unfilled trade display fix in dashboard Trades tab
2. Polymarket fee verification (confirmed accurate from official docs)
3. v0.1.9 min-shares retry fix (already deployed)
4. Full fee table from official Polymarket documentation

## FILE PATHS
- e:\projects\products\crypto5min-polytrader\README.md
- e:\projects\products\crypto5min-polytrader\SETUP_GUIDE.md
- e:\projects\products\crypto5min-polytrader\METRICS_AND_CAVEATS.md
- e:\projects\products\crypto5min-polytrader\SALES_COPY.md
- e:\projects\products\crypto5min-polytrader\.env.example
- e:\projects\products\crypto5min-polytrader\tools\release_zip.ps1
- e:\projects\products\crypto5min-polytrader\templates\partials\trades.html (already fixed)
