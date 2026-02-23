"""Dashboard audit v2 - correct file paths."""
import json, sys
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

print("=== STATE.JSON ===")
state = load("state.json", {})
if state:
    print(f"Keys: {list(state.keys())}")
    print(f"  status: {state.get('status')}")
    print(f"  ts: {state.get('ts')}")
    redeem = state.get('redeem')
    print(f"  redeem: {redeem}")
    rec = state.get('redeem_reconcile')
    print(f"  redeem_reconcile: {rec}")
else:
    print("  state.json is EMPTY or MISSING")

print()
print("=== OPS LOG (last 5) ===")
ops = load("poly_ops.json", [])
print(f"Total ops events: {len(ops)}")
for e in [x for x in ops if isinstance(x,dict)][-5:]:
    result = e.get('result')
    ok_top = e.get('ok')
    ok_in_result = result.get('ok') if isinstance(result, dict) else None
    print(f"  ts={e.get('ts')} | action={e.get('action')} | ok_top={ok_top} | ok_result={ok_in_result} | result={result}")

print()
print("=== WINS WITH REDEEM STATUS ===")
trades = load("poly_trades.json", [])
wins = [t for t in trades if isinstance(t,dict) and t.get('resolved')=='win']
print(f"Total wins: {len(wins)}")
by_redeemstatus = {}
for t in wins:
    rs = t.get('redeem_status', 'none')
    by_redeemstatus[rs] = by_redeemstatus.get(rs, 0) + 1
print(f"  By redeem_status: {by_redeemstatus}")
# Show wins that are not yet redeemed
unredeemed = [t for t in wins if t.get('redeem_status') not in ('success',)]
print(f"  Unredeemed wins: {len(unredeemed)}")
for t in unredeemed[-3:]:
    print(f"    window_slug={t.get('window_slug')} | redeem_status={t.get('redeem_status')} | resolved_ts={t.get('resolved_ts')}")

print()
print("=== WIN_UNFILLED TRADES ===")
wu = [t for t in trades if isinstance(t,dict) and t.get('resolved')=='win_unfilled']
print(f"Total win_unfilled: {len(wu)}")
for t in wu:
    print(f"  window_slug={t.get('window_slug')} | redeem_status={t.get('redeem_status')} | order_status={t.get('order_status')}")

print()
print("=== ORPHAN REDEEMED (TTL cache) ===")
orphan = load("orphan_redeemed.json", {})
print(f"Type: {type(orphan).__name__}")
if isinstance(orphan, dict):
    print(f"  Keys count: {len(orphan)}")
    for k,v in list(orphan.items())[:3]:
        print(f"    {k}: {v}")
elif isinstance(orphan, list):
    print(f"  (OLD FORMAT: list with {len(orphan)} items)")
    for item in orphan[:3]:
        print(f"    {item}")
