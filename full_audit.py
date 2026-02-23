"""
Check redeemable field in positions + current trades state + force redeem
"""
import sys, os, json, time, requests
sys.path.insert(0, '/app/src')

with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from crypto5min_polytrader.polymarket_account import fetch_positions, derive_address

pk = os.environ.get('C5_POLY_PRIVATE_KEY', '')
address = derive_address(pk)

# Fetch all positions
positions = fetch_positions(address, limit=500)
print(f"Total positions returned: {len(positions)}")

# Check redeemable
redeemable = [p for p in positions if p.get('redeemable') == True or str(p.get('redeemable','')).lower() == 'true']
has_value = [p for p in positions if float(p.get('currentValue') or 0) > 0.001]
has_size = [p for p in positions if float(p.get('size') or 0) > 0.1]

print(f"  redeemable=True: {len(redeemable)}")
print(f"  currentValue > 0: {len(has_value)}")
print(f"  size > 0.1: {len(has_size)}")

if redeemable:
    print("\n=== REDEEMABLE POSITIONS ===")
    for p in redeemable:
        title = (p.get('title') or p.get('slug') or '')[:55]
        size = float(p.get('size') or 0)
        cur_val = float(p.get('currentValue') or 0)
        outcome = p.get('outcome','')
        cid = (p.get('conditionId') or '')[:25]
        print(f"  [{outcome}] {title}")
        print(f"    size={size:.2f}  currentValue=${cur_val:.4f}  conditionId={cid}...")

if has_value:
    print("\n=== POSITIONS WITH VALUE ===")
    for p in has_value:
        title = (p.get('title') or p.get('slug') or '')[:55]
        size = float(p.get('size') or 0)
        cur_val = float(p.get('currentValue') or 0)
        cur_price = float(p.get('curPrice') or 0)
        outcome = p.get('outcome','')
        cid = (p.get('conditionId') or '')[:25]
        print(f"  [{outcome}] {title}")
        print(f"    size={size:.2f}  curPrice={cur_price:.4f}  value=${cur_val:.4f}")
        print(f"    conditionId: {cid}...")

# Show current trades state
print()
print("=== CURRENT TRADES STATE ===")
trades = json.load(open('/app/logs/poly_trades.json'))
now_ts = int(time.time())

by_resolved = {}
for t in trades:
    r = t.get('resolved') or 'none'
    by_resolved[r] = by_resolved.get(r, 0) + 1
print(f"Total trades: {len(trades)}")
print(f"By resolved: {by_resolved}")
print(f"Has redeem_tx_hash: {len([t for t in trades if t.get('redeem_tx_hash')])}")

# Most recent 6 trades
print("\nMost recent 6 trades:")
for t in trades[-6:]:
    q = (t.get('question') or t.get('window_slug') or '')[:50]
    r = t.get('resolved', '?')
    redeem_tx = (t.get('redeem_tx_hash') or '')[:16]
    age_min = (now_ts - t.get('placed_ts', now_ts)) / 60
    usdc = t.get('usdc', 0)
    print(f"  {q}")
    print(f"    resolved={r}  redeem_tx={redeem_tx or 'none'}  ${usdc}  {age_min:.1f}min ago")

# Current snapshot
snap = json.load(open('/app/logs/poly_snapshot.json'))
snap_age = (now_ts - snap.get('ts', now_ts)) / 60
print(f"\nSnapshot: equity=${snap.get('total_equity_usdc',0):.2f}  clob=${snap.get('clob_balance_usdc',0):.2f}  pos=${snap.get('positions_value_usdc',0):.2f}  ({snap_age:.1f}min old)")

# Force a fresh snapshot to see live balance
print("\n=== LIVE CLOB BALANCE ===")
try:
    from crypto5min_polytrader.polymarket_account import clob_balance_usdc
    sig = int(os.environ.get('C5_POLY_SIGNATURE_TYPE','0') or 0)
    funder = os.environ.get('C5_POLY_FUNDER_ADDRESS','') or None
    bal = clob_balance_usdc(pk, signature_type=sig, funder=funder)
    print(f"  Live CLOB balance: ${bal:.4f}")
    print(f"  Live positions val: ${0:.4f}  (all currentValue=0 in API)")
    print(f"  Live total: ${bal:.4f}")
except Exception as e:
    print(f"  Error: {e}")
