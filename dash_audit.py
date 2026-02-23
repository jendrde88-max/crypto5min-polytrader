"""Dashboard audit script - check live data state on VPS."""
import json, sys, os
from pathlib import Path

LOG_DIR = Path("/app/logs")

def load(name, default=None):
    p = LOG_DIR / name
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text())
    except Exception as e:
        print(f"  ERROR loading {name}: {e}")
        return default

print("=== TRADES ===")
trades = load("poly_trades.json", [])
print(f"Total trades: {len(trades)}")
if trades:
    last5 = [t for t in trades if isinstance(t, dict)][-5:]
    for t in last5:
        print(f"  resolved={t.get('resolved')} | window_slug={t.get('window_slug','MISSING')} | redeem_status={t.get('redeem_status','none')} | order_status={t.get('order_status')}")
    # Count
    by_res = {}
    for t in trades:
        if isinstance(t, dict):
            r = t.get('resolved','pending')
            by_res[r] = by_res.get(r,0)+1
    print(f"  By resolved: {by_res}")
    # Check how many have window_slug
    has_slug = sum(1 for t in trades if isinstance(t,dict) and t.get('window_slug'))
    print(f"  Have window_slug: {has_slug}/{len(trades)}")

print()
print("=== SNAPSHOT ===")
snap = load("poly_snapshot.json")
if snap:
    print(f"Fields: {list(snap.keys())}")
    for k,v in snap.items():
        print(f"  {k}: {v}")
else:
    print("  NO SNAPSHOT FILE")

print()
print("=== STATE ===")
state = load("poly_state.json", {})
if state:
    print(f"Keys: {list(state.keys())}")
    redeem = state.get('redeem')
    print(f"  redeem: {redeem}")
    rec = state.get('redeem_reconcile')
    print(f"  redeem_reconcile: {rec}")
else:
    print("  NO STATE FILE")

print()
print("=== OPS LOG ===")
ops = load("poly_ops.json", [])
print(f"Total ops events: {len(ops)}")
if ops:
    for e in [x for x in ops if isinstance(x,dict)][-5:]:
        print(f"  {e.get('ts','')} | {e.get('action','?')} | ok={e.get('ok')} | result_keys={list(e.get('result',{}).keys()) if isinstance(e.get('result'),dict) else e.get('result')}")

print()
print("=== EQUITY SERIES ===")
equity = load("poly_equity.json", [])
print(f"Equity points: {len(equity)}")
if equity and isinstance(equity, list) and equity:
    first = equity[0]
    last_e = equity[-1]
    print(f"  First: ts={first.get('ts')} equity={first.get('equity')}")
    print(f"  Last:  ts={last_e.get('ts')} equity={last_e.get('equity')}")

print()
print("=== LAST TRADE ===")
last_trade = load("poly_last_trade.json", {})
if last_trade:
    print(f"Fields: {list(last_trade.keys())}")
    for k,v in list(last_trade.items())[:10]:
        print(f"  {k}: {v}")
else:
    print("  NO LAST TRADE FILE")

print()
print("=== WIN/LOSS STATS CHECK ===")
# Replicate resolution.load_stats() manually
wins = losses = pending = wins_u = losses_u = 0
skipped_no_slug = 0
for t in [x for x in trades if isinstance(x, dict)]:
    if not t.get('window_slug'):
        skipped_no_slug += 1
        continue
    r = t.get('resolved')
    if r == 'win': wins += 1
    elif r == 'loss': losses += 1
    elif r == 'win_unfilled': wins_u += 1
    elif r == 'loss_unfilled': losses_u += 1
    else: pending += 1

total_filled = wins + losses
wr = round(wins/total_filled*100, 1) if total_filled > 0 else 0
print(f"wins={wins} losses={losses} pending={pending} wins_unfilled={wins_u} losses_unfilled={losses_u}")
print(f"Skipped (no window_slug): {skipped_no_slug}")
print(f"Win rate (filled only): {wr}%  ({wins}/{total_filled})")
