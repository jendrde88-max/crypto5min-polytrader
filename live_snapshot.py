"""
Live cross-reference: force a fresh snapshot then compare.
"""
import sys, os, json, time, requests
sys.path.insert(0, '/app/src')

with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

now_ts = time.time()

# 1. Stale snapshot
snap = json.load(open('/app/logs/poly_snapshot.json'))
snap_age_min = (now_ts - snap.get('ts', now_ts)) / 60
print(f"=== STALE SNAPSHOT (from {snap_age_min:.1f} min ago) ===")
print(f"  active_positions:    {snap.get('active_positions')}")
print(f"  positions_value:     ${snap.get('positions_value_usdc', 0):.2f}")
print(f"  clob_balance:        ${snap.get('clob_balance_usdc', 0):.2f}")
print(f"  total_equity:        ${snap.get('total_equity_usdc', 0):.2f}")
print(f"  unrealized_pnl:      ${snap.get('unrealized_pnl_usdc', 0):.2f}")
print()

# 2. Force fresh snapshot
print("=== FRESH SNAPSHOT (building now...) ===")
try:
    from crypto5min_polytrader.polymarket_account import snapshot_from_env
    fresh = snapshot_from_env()
    if fresh:
        print(f"  active_positions:    {fresh.active_positions}")
        print(f"  positions_value:     ${fresh.positions_value_usdc:.2f}")
        print(f"  clob_balance:        ${fresh.clob_balance_usdc:.2f}")
        print(f"  total_equity:        ${fresh.clob_balance_usdc + fresh.positions_value_usdc:.2f}")
        print(f"  unrealized_pnl:      ${fresh.unrealized_pnl_usdc:.2f}")
        print(f"  cost_basis:          ${fresh.cost_basis_usdc:.2f}")
        print()
        
        # Show what changed
        old_eq = snap.get('total_equity_usdc', 0)
        new_eq = fresh.clob_balance_usdc + fresh.positions_value_usdc
        print(f"  CHANGE vs snapshot:  ${new_eq - old_eq:+.2f}")
    else:
        print("  snapshot_from_env returned None (missing private key?)")
except Exception as e:
    print(f"  Error: {e}")
    import traceback; traceback.print_exc()

# 3. Check recent app.log for redeem activity
print()
print("=== RECENT APP.LOG (last 30 lines) ===")
import subprocess
r = subprocess.run(['tail', '-30', '/app/logs/app.log'], capture_output=True, text=True)
for line in r.stdout.splitlines():
    if any(x in line for x in ['redeem', 'REDEEM', 'win', 'resolve', 'snapshot', 'ERROR', 'WARN', 'balance', 'TRADE', 'FILL']):
        print(f"  {line.strip()[-120:]}")
