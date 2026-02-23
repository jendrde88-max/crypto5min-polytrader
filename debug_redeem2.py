"""
Deep debug: why is process_auto_redeem skipping?
Also fetch live positions from Polymarket API to see what's there.
"""
import sys, os, json, time
sys.path.insert(0, '/app/src')

# Load env
with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from crypto5min_polytrader.polymarket_redeem import (
    is_redeem_enabled,
    select_redeem_candidates_from_trades,
    find_redeem_candidates,
    _find_orphan_redeemable_positions,
)

print(f"is_redeem_enabled: {is_redeem_enabled()}")

trades = json.load(open('/app/logs/poly_trades.json'))
now_ts = int(time.time())
print(f"Now: {now_ts}, Total trades: {len(trades)}")

# Check what select_redeem_candidates_from_trades finds
candidates = select_redeem_candidates_from_trades(trades, max_trades=50, now=now_ts, retry_sec=60)
print(f"\nselect_redeem_candidates_from_trades: {len(candidates)} candidates")
for c in candidates[:10]:
    q = (c.get('question') or c.get('window_slug') or '')[:55]
    ost = c.get('order_status')
    rec = c.get('last_reconciled_ts', -1)
    usdc = c.get('usdc')
    print(f"  order_status={ost} last_reconciled={rec} ${usdc}  {q}")

# Check orphans
print("\n--- Orphan check ---")
known_cids = set(t.get('condition_id','') for t in trades if t.get('condition_id'))
print(f"Known condition_ids: {len(known_cids)}")
try:
    orphans = _find_orphan_redeemable_positions(known_cids)
    print(f"Orphan positions found: {len(orphans)}")
    for o in orphans[:5]:
        print(f"  {o}")
except Exception as e:
    print(f"Error fetching orphans: {e}")
    import traceback; traceback.print_exc()

# Try fetching positions directly via API
print("\n--- Direct Polymarket positions API ---")
try:
    import requests
    wallet = os.environ.get('C5_POLY_WALLET_ADDRESS') or os.environ.get('POLY_WALLET_ADDRESS', '')
    print(f"Wallet: {wallet[:15]}...")
    url = f"https://data-api.polymarket.com/positions?user={wallet}&sizeThreshold=0.01&limit=50"
    r = requests.get(url, timeout=15)
    data = r.json()
    positions = data if isinstance(data, list) else data.get('data', data.get('positions', []))
    print(f"API returned {len(positions)} positions")
    total_val = 0
    for p in positions[:10]:
        slug = (p.get('market') or p.get('conditionId') or p.get('slug',''))[:40]
        size = float(p.get('size', p.get('shares', 0)) or 0)
        val = float(p.get('value', p.get('currentValue', 0)) or 0)
        price = float(p.get('curPrice', p.get('price', 0)) or 0)
        cid = p.get('conditionId','')[:20]
        cash_out = float(p.get('cashPnl', 0) or 0)
        total_val += val
        print(f"  {slug}")
        print(f"    size={size:.2f} price={price:.3f} value=${val:.2f} conditionId={cid}...")
        print(f"    raw keys: {list(p.keys())[:8]}")
    print(f"Total value: ${total_val:.2f}")
except Exception as e:
    print(f"API error: {e}")
    import traceback; traceback.print_exc()
