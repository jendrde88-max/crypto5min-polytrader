"""
Cross-reference: Dashboard state vs poly_snapshot vs trades log vs Polymarket API
"""
import sys, os, json, time, requests
sys.path.insert(0, '/app/src')

with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

now_ts = int(time.time())

# 1. poly_snapshot.json (updated by bg_loop)
snap = json.load(open('/app/logs/poly_snapshot.json'))
snap_age_min = (now_ts - snap.get('ts', now_ts)) / 60
print("=== poly_snapshot.json ===")
print(f"  Age: {snap_age_min:.1f} min ago")
print(f"  active_positions: {snap.get('active_positions')}")
print(f"  clob_balance_usdc: ${snap.get('clob_balance_usdc', 0):.4f}")
print(f"  positions_value_usdc: ${snap.get('positions_value_usdc', 0):.4f}")
print(f"  cost_basis_usdc: ${snap.get('cost_basis_usdc', 0):.4f}")
print(f"  unrealized_pnl_usdc: ${snap.get('unrealized_pnl_usdc', 0):.4f}")
print(f"  total_equity_usdc: ${snap.get('total_equity_usdc', 0):.4f}")

# 2. poly_equity.json (equity history)
try:
    eq = json.load(open('/app/logs/poly_equity.json'))
    if isinstance(eq, list) and eq:
        last = eq[-1]
        eq_age = (now_ts - last.get('ts', now_ts)) / 60
        print(f"\n=== poly_equity.json (last entry) ===")
        print(f"  Age: {eq_age:.1f} min ago")
        for k, v in sorted(last.items()):
            print(f"  {k}: {v}")
except Exception as e:
    print(f"\npoly_equity.json error: {e}")

# 3. poly_trades.json — count by order_status
trades = json.load(open('/app/logs/poly_trades.json'))
from collections import Counter
status_counts = Counter(t.get('order_status', 'none') for t in trades)
resolved_counts = Counter(t.get('resolved', 'none') for t in trades if t.get('resolved'))
redeemed_count = len([t for t in trades if t.get('redeem_tx_hash')])
print(f"\n=== poly_trades.json ({len(trades)} total) ===")
print(f"  order_status: {dict(status_counts)}")
print(f"  resolved: {dict(resolved_counts)}")
print(f"  has redeem_tx_hash: {redeemed_count}")

# Open = filled, no redeemed, resolved=win
open_wins = [t for t in trades if t.get('order_status')=='filled' 
             and t.get('resolved')=='win' 
             and not t.get('redeem_tx_hash')]
print(f"  Filled wins NOT yet redeemed: {len(open_wins)}")

# 4. Live Polymarket API
wallet = '0xf8764f91A3b8f6bF111e9EC5c670B541415D8975'
print(f"\n=== Polymarket data-api (live) ===")
try:
    url = f"https://data-api.polymarket.com/positions?user={wallet}&sizeThreshold=0.01&limit=100"
    r = requests.get(url, timeout=15)
    data = r.json()
    positions = data if isinstance(data, list) else data.get('data', [])
    live_positions = [p for p in positions if float(p.get('curPrice', p.get('price', 0)) or 0) > 0.01]
    total_val = sum(float(p.get('value', 0) or 0) for p in positions)
    live_val = sum(float(p.get('value', 0) or 0) for p in live_positions)
    print(f"  All positions: {len(positions)}")
    print(f"  With price > 0.01: {len(live_positions)}")
    print(f"  Total value (all): ${total_val:.4f}")
    print(f"  Total value (live): ${live_val:.4f}")
    for p in live_positions:
        title = (p.get('title') or p.get('market') or '')[:50]
        size = float(p.get('size', 0) or 0)
        val = float(p.get('value', 0) or 0)
        price = float(p.get('curPrice', p.get('price', 0)) or 0)
        outcome = p.get('outcome', '')
        print(f"    [{outcome}] {title}")
        print(f"      {size:.2f}sh @ {price:.3f} = ${val:.2f}")
except Exception as e:
    print(f"  API error: {e}")
    import traceback; traceback.print_exc()

# 5. Summary comparison
print("\n=== CROSS-REFERENCE SUMMARY ===")
print(f"  Snapshot positions value:    ${snap.get('positions_value_usdc', 0):.2f}")
print(f"  Snapshot CLOB balance:       ${snap.get('clob_balance_usdc', 0):.2f}")
print(f"  Snapshot total equity:       ${snap.get('total_equity_usdc', 0):.2f}")
print(f"  Snapshot active positions:   {snap.get('active_positions')}")
print(f"  API live position value:     ${live_val:.2f}  ({len(live_positions)} positions)")
print(f"  Diff (snapshot vs api):      ${snap.get('positions_value_usdc', 0) - live_val:.2f}")
