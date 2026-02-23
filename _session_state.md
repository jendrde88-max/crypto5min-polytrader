# CRITICAL SESSION STATE - DO NOT DELETE

## VPS & ACCESS
- Workspace: e:\projects\products\crypto5min-polytrader
- VPS: root@65.109.240.249, container: crypto5min-polytrader, port 8602:8601
- Dashboard password: 1Bubby1!1

## CURRENT CONFIG (runtime_config.json on VPS)
- C5_POLY_BET_MODE: percent
- C5_POLY_BET_PERCENT: 50.0  <-- THIS IS THE PROBLEM, SHOULD BE 10
- C5_POLY_HIGH_RISK_MODE: true
- C5_POLY_EXPERT_MODE: false
- C5_CONFIDENCE_THRESHOLD: 0.5  <-- TOO LOW, ML trades at barely 50%
- Snipe mode: enabled (C5_SNIPE_ENABLED)
- Kelly fix already deployed (uses base_ask not price for edge)

## USER'S PROBLEM
Bot went from 12 wins in a row (snipe trades, small bets $8-$39) to massive losses.
The losses are because:
1. BET_PERCENT is 50% (not 10%) - bets half the account each trade
2. ML predictions have only ~50-51% confidence - basically coin flips
3. Threshold is 0.5 so even 50.1% confidence triggers a trade
4. Losing trades at 50% per trade = account halves each loss

## TRADE DATA ANALYSIS
Win streak (11:30-12:20): All small bets, mostly UP, snipe mode trades
Loss streak (12:30-13:40): Big bets ($45-$112), mix UP/DOWN, ML prediction trades

## WHAT USER WANTS
- 80% win rate like snipe mode promises
- Not by reducing trades, but by making predictions more accurate
- The snipe mode WAS working great (the win streak)
- ML prediction mode is dragging it down

## FIXES NEEDED
1. Set C5_POLY_BET_PERCENT back to 10 (from 50)
2. Raise C5_CONFIDENCE_THRESHOLD to 0.55 or higher
   - This means ML only trades when model is confident (>55%)
   - Snipe trades already have high confidence (80-90%) so they'll still fire
3. Consider: make snipe the PRIMARY strategy, ML secondary
4. Consider: different bet sizes for ML vs snipe (snipe = bigger, ML = smaller)

## FILES TO INVESTIGATE
- src/crypto5min_polytrader/runner.py - main loop, calls predict + execute
- src/crypto5min_polytrader/polymarket_exec.py - bet sizing, kelly fix
- src/crypto5min_polytrader/window.py - snipe mode, late entry logic
- src/crypto5min_polytrader/model.py - CNN-LSTM model confidence
- src/crypto5min_polytrader/config.py - defaults
- src/crypto5min_polytrader/runtime_config.py - runtime config allowlist

## KELLY FIX (ALREADY DEPLOYED)
- polymarket_exec.py: Kelly uses base_ask instead of price (ask+buffer) for edge
- Added C5_POLY_KELLY_MIN_PCT (default 2%) floor for tiny Kelly bets
- runtime_config.py: Added C5_POLY_KELLY_MIN_PCT to allowlist
- BUT: Kelly was never activated because bet_mode stayed "percent"

## VERSION
- v0.2.0 ZIP built at dist\Crypto5min_PolyTrader_v0.2.0.zip
- CHANGELOG_v0.2.0.md created
- All docs updated for unfilled trade display + fee verification

## INTERNET RESEARCH RESULTS (Feb 16, 2026)

### CRITICAL FEE UPDATE
- Polymarket docs (https://docs.polymarket.com/polymarket-learn/trading/fees) now say:
  - "The vast majority of Polymarket markets have no trading fees"  
  - Markets WITH fees: "15-minute crypto markets", NCAAB, Serie A
  - **5-minute crypto markets are NOT listed as having fees!**
  - Only 15-minute crypto markets listed as having taker fees
  - This is a CHANGE from our v0.1.9/v0.2.0 research where we confirmed 5-min had fees
  - Fee table (for 15-min): max 1.56% at $0.50 price, symmetric curve
  - Fee formula: fee = baseRate × min(price, 1-price) × size
  - Maker rebate: 20% of taker fees redistributed daily to makers

### CLOB API Info
- py-clob-client v0.34.5 (latest)
- Minimum order size: 5 shares (confirmed from examples)
- Signature types: 0=EOA, 1=POLY_PROXY (email/Magic), 2=POLY_GNOSIS_SAFE
- Prices 0.00 to 1.00 USDC
- All orders are limit orders (can be marketable)
- Exchange audited by Chainsecurity

### Key URLs
- Fees: https://docs.polymarket.com/polymarket-learn/trading/fees
- Maker Rebates: https://docs.polymarket.com/polymarket-learn/trading/maker-rebates-program
- CLOB Intro: https://docs.polymarket.com/developers/CLOB/introduction
- py-clob-client: https://github.com/Polymarket/py-clob-client

## CHANGES MADE THIS SESSION (v0.2.1)
1. Fixed VPS runtime_config.json: BET_PERCENT 50→10, HIGH_RISK off, MAX_USDC 100, THRESHOLD 0.55
2. Added snipe_bet_multiplier to PolyExecConfig (C5_POLY_SNIPE_BET_MULTIPLIER, default 2.0)
3. Added snipe param to trade_window() and _place_order()
4. Added snipe bet multiplier logic in _place_order() bet sizing
5. Passed snipe=True from web.py snipe cadence
6. Added C5_POLY_SNIPE_BET_MULTIPLIER to runtime_config.py allowlist
7. Deployed all 3 files to VPS, restarted container - verified healthy

## FILES CHANGED THIS SESSION
- src/crypto5min_polytrader/polymarket_exec.py - snipe_bet_multiplier config + trade_window snipe param + sizing logic
- src/crypto5min_polytrader/web.py - snipe=True in snipe cadence trade_window call
- src/crypto5min_polytrader/runtime_config.py - added C5_POLY_SNIPE_BET_MULTIPLIER to allowlist

## TODO FOR v0.2.1 RELEASE
1. Create CHANGELOG_v0.2.1.md
2. Update README.md - add snipe bet multiplier, update fee info (5-min may be fee-free now!)
3. Update SETUP_GUIDE.md - add snipe bet multiplier setting
4. Update METRICS_AND_CAVEATS.md - update fee info
5. Update SALES_COPY.md - emphasize snipe mode accuracy
6. Update .env.example - add C5_POLY_SNIPE_BET_MULTIPLIER
7. Update release_zip.ps1 for v0.2.1
8. Build ZIP

## CODE ANALYSIS RESULTS
### runner.py (337 lines)
- predict_latest() at line 158: ML prediction, returns direction/p_up/confidence
- predict_snipe() at line 226: Snipe prediction, returns snipe=True, confidence 65-95% via sigmoid
- Snipe fires when BTC delta > snipe_min_delta_pct (0.02%) in last 10s before close
- ML confidence is often 0.50-0.51 (essentially coin flip)
- The main trading loop calls BOTH predict_latest and predict_snipe
- Snipe is a "second pass" - runs after ML, won't duplicate

### The Problem
1. BET_PERCENT=50 (should be 10) - bets half account per trade
2. CONFIDENCE_THRESHOLD=0.5 - ML trades at 50.1% (coin flip level)
3. Snipe trades had 65-95% confidence (the 12 wins in a row)
4. ML trades had ~50% confidence (the losses)
5. Both use SAME bet sizing (50% of balance), so ML losses are huge

### Implementation Plan
1. Fix config: BET_PERCENT=10, HIGH_RISK=false, THRESHOLD=0.55
2. Add snipe/ML differentiated betting (snipe=higher%, ML=lower%)
3. This will let snipe trades stay aggressive while ML trades are conservative
4. The polymarket_exec.py already gets the prediction dict - can check for 'snipe' key
5. Config for this: C5_POLY_SNIPE_BET_MULTIPLIER (e.g. 2.0 = snipe bets 2x normal)
