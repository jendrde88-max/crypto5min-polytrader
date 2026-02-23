#!/usr/bin/env python3
"""Quick paper PnL integration test for VPS."""
from crypto5min_polytrader.paper_pnl import PaperLedger

ledger = PaperLedger(starting_cash=10000.0)
snap = ledger.snapshot()
print(f"INIT: cash={snap['cash']}, equity={snap['equity']}")

trade = {"condition_id": "test123", "usdc": 50.0, "price": 0.6, "side": "buy", "dry_run": True, "window_slug": "test-slug-1"}
ledger.fill(trade)
print(f"FILLED: status={trade.get('order_status')}, size={trade.get('filled_size')}, price={trade.get('avg_fill_price')}")

snap2 = ledger.snapshot()
print(f"AFTER FILL: cash={snap2['cash']}, equity={snap2['equity']}, trades={snap2['trade_count']}")

# Test resolve win
trade["resolved"] = "win"
ledger.resolve(trade)
snap3 = ledger.snapshot()
print(f"AFTER WIN: cash={snap3['cash']}, equity={snap3['equity']}, realized_pnl={snap3['realized_pnl']}")
print(f"  win_count={snap3['win_count']}, loss_count={snap3['loss_count']}, win_rate={snap3['win_rate']}")

# Test reset
ledger.reset()
snap4 = ledger.snapshot()
print(f"AFTER RESET: cash={snap4['cash']}, equity={snap4['equity']}, trades={snap4['trade_count']}")

print("\nALL OK")
