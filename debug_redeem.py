"""
Show what find_redeem_candidates and orphan finder return.
Helps understand why nothing is redeemable.
"""
import sys, json, os
sys.path.insert(0, '/app/src')
sys.path.insert(0, '/app/src/crypto5min_polytrader')

from datetime import datetime, timezone
import time

now_ts = int(time.time())

# 1. Show what select_redeem_candidates_from_trades says
from polymarket_redeem import (
    select_redeem_candidates_from_trades,
    find_redeem_candidates,
    _find_orphan_redeemable_positions,
)

trades = json.load(open('/app/logs/poly_trades.json'))
print(f"Total trades: {len(trades)}")

candidates = select_redeem_candidates_from_trades(trades, max_trades=50, now=now_ts, retry_sec=60)
print(f"\nselect_redeem_candidates_from_trades → {len(candidates)} candidates")
for c in candidates:
    q = (c.get('question') or c.get('window_slug') or '')[:50]
    print(f"  {q} | usdc={c.get('usdc')} | order_status={c.get('order_status')}")

# 2. Show orphan positions
print("\n--- Orphan redeemable positions ---")
try:
    known_cids = set(t.get('condition_id','') for t in trades if t.get('condition_id'))
    print(f"Known condition_ids in trades: {len(known_cids)}")
    orphans = _find_orphan_redeemable_positions(known_cids)
    print(f"Orphan redeemable positions: {len(orphans)}")
    for o in orphans:
        print(f"  {o}")
except Exception as e:
    print(f"orphan error: {e}")
    import traceback; traceback.print_exc()

# 3. Try find_redeem_candidates
print("\n--- find_redeem_candidates ---")
try:
    result = find_redeem_candidates(trades=trades, max_trades=50, now=now_ts, retry_sec=60)
    print(f"find_redeem_candidates → {len(result)} items")
    for r in result:
        q = (r.get('question') or r.get('window_slug') or '')[:50]
        print(f"  {q}")
except Exception as e:
    print(f"find_redeem_candidates error: {e}")
    import traceback; traceback.print_exc()
