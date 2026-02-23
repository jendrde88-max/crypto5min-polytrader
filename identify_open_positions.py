#!/usr/bin/env python3
"""
Identify the exact 5 open positions and cross-reference with trades log.
"""
import sys, os, json, requests
sys.path.insert(0, '/app/src')

from crypto5min_polytrader.polymarket_account import fetch_positions

# Load trades log
TRADES_FILE = '/app/logs/poly_trades.json'
try:
    with open(TRADES_FILE) as f:
        trades = json.load(f)
    print(f"Loaded {len(trades)} trades from log")
except Exception as e:
    trades = []
    print(f"No trades file: {e}")

# Build lookup by condition_id and window_slug
trades_by_cid = {}
trades_by_slug = {}
for i, t in enumerate(trades):
    cid = t.get('condition_id', '')
    slug = t.get('window_slug', '')
    if cid:
        trades_by_cid[cid] = (i, t)
    if slug:
        if slug not in trades_by_slug:
            trades_by_slug[slug] = []
        trades_by_slug[slug].append((i, t))

# Fetch live positions
wallet = os.environ.get('C5_POLY_WALLET_ADDRESS', '')
if not wallet:
    # Try to get from snapshot
    try:
        snap = json.load(open('/app/logs/poly_snapshot.json'))
        wallet = snap.get('wallet', '')
    except:
        pass

print(f"Wallet: {wallet}")

resp = requests.get(f"https://data-api.polymarket.com/positions?user={wallet}&limit=500&sizeThreshold=0.01")
all_positions = resp.json() if resp.status_code == 200 else []
print(f"Total positions from API: {len(all_positions)}")

# Find positions with currentValue > 0
live = [p for p in all_positions if float(p.get('currentValue', 0)) > 0]
print(f"\n=== {len(live)} LIVE POSITIONS (currentValue > 0) ===")
for p in live:
    cid = p.get('conditionId', '')
    slug = p.get('title', p.get('slug', ''))
    val = float(p.get('currentValue', 0))
    size = float(p.get('size', 0))
    outcome = p.get('outcome', '')
    market = p.get('market', p.get('question', slug))[:60] if p.get('market') or p.get('question') else slug[:60]
    redeemable = p.get('redeemable', False)
    
    print(f"\n  Market: {market}")
    print(f"  Outcome: {outcome}  |  Value: ${val:.4f}  |  Size: {size:.2f}")
    print(f"  conditionId: {cid}")
    print(f"  redeemable: {redeemable}")
    
    # Check if in trades log
    if cid in trades_by_cid:
        idx, t = trades_by_cid[cid]
        print(f"  TRADES LOG MATCH (index {idx}): order_status={t.get('order_status')} resolved={t.get('resolved')} usdc={t.get('usdc')}")
        print(f"    window_slug={t.get('window_slug')} placed_ts={t.get('placed_ts')}")
    else:
        # Try slug match
        title_lower = (p.get('title') or '').lower()
        found = False
        for slug_key, trade_list in trades_by_slug.items():
            if slug_key.lower() in title_lower or title_lower in slug_key.lower():
                for idx, t in trade_list:
                    print(f"  SLUG MATCH ({slug_key}): order_status={t.get('order_status')} resolved={t.get('resolved')} usdc={t.get('usdc')}")
                    found = True
        if not found:
            print(f"  *** NO MATCH IN TRADES LOG (orphan position) ***")

# Now show all "pending" trades in log (filled, not yet resolved)
print("\n\n=== TRADES LOG: filled + not resolved ===")
pending_count = 0
for i, t in enumerate(trades):
    status = t.get('order_status', '')
    resolved = t.get('resolved', None)
    redeem_tx = t.get('redeem_tx_hash', '')
    if status == 'filled' and not resolved and not redeem_tx:
        pending_count += 1
        print(f"  [{i}] {t.get('window_slug')} | usdc={t.get('usdc')} | placed={t.get('placed_ts')} | cid={t.get('condition_id','')[:20]}...")

if pending_count == 0:
    print("  (none - all trades are resolved or have redeem tx)")

# Also check trades with resolved=loss but position still has value  
print("\n=== TRADES LOG: resolved=loss but position still live? ===")
for i, t in enumerate(trades):
    cid = t.get('condition_id', '')
    if cid and cid in {p['conditionId'] for p in live}:
        print(f"  [{i}] {t.get('window_slug')} resolved={t.get('resolved')} order_status={t.get('order_status')} redeem_tx={t.get('redeem_tx_hash','')[:20]}")

print("\nDone.")
