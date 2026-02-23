"""Deeper bot status check — recent trades detail."""
import json, time

trades = json.load(open("/app/logs/poly_trades.json"))
now = time.time()

print(f"=== LAST 10 TRADES ===")
for t in trades[-10:]:
    age = int(now - t.get("placed_ts", 0))
    slug = t.get("window_slug", "?")
    d = t.get("direction", "?")
    res = t.get("resolution")
    st = t.get("order_status", "?")
    fs = t.get("filled_size", 0)
    bet = t.get("bet_amount", 0)
    eqy = t.get("equity_after", "?")
    print(f"  {slug[-25:]} dir={d} res={res} status={st} bet=${bet} filled=${fs} equity={eqy} ({age//60}min ago)")

print(f"\n=== RESOLUTION BREAKDOWN (all {len(trades)} trades) ===")
res_all = {}
for t in trades:
    r = str(t.get("resolution"))
    res_all[r] = res_all.get(r, 0) + 1
for k, v in sorted(res_all.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print(f"\n=== ORDER STATUS BREAKDOWN (last 20) ===")
for t in trades[-20:]:
    st = t.get("order_status", "?")
    slug = t.get("window_slug", "?")[-20:]
    age = int(now - t.get("placed_ts", 0))
    fs = t.get("filled_size", 0)
    res = t.get("resolution")
    print(f"  {slug} st={st} filled=${fs} res={res} ({age//60}min)")

# Check USDC balance from state
import os
state_path = "/app/logs/state.json"
if os.path.exists(state_path):
    state = json.load(open(state_path))
    print(f"\n=== STATE ===")
    print(f"  usdc_balance: {state.get('usdc_balance', '?')}")
    print(f"  poly_equity: {state.get('poly_equity', '?')}")
    print(f"  gas_pol: {state.get('gas_pol', '?')}")
