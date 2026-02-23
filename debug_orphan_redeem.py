#!/usr/bin/env python3
"""Debug the exact return values from process_auto_redeem for the orphan positions."""
import sys, json
sys.path.insert(0, '/app/src')

ORPHAN_FILE = '/app/logs/orphan_redeemed.json'
STUCK_CIDS = [
    "0x78e6508b6dcf4ca3f0419a6343bc2413bb6315cbbfc600af8dc05603aca75dd1",
    "0x5d8e5293632061a2972ad1ddc84c5030fddb29f5f884e2f43ecd4509af55b499",
    "0xc98e31d95733702687301fbb701ec462c0a64b46a8dfd5d8550b05785286b4b2",
    "0x819b3f58db41c9cc097db7343906fe0c37f2f206b425a2aab1a40be2911c5ae3",
]

# Clear the cache again
with open(ORPHAN_FILE) as f:
    attempted = json.load(f)
print(f"Currently in already_attempted: {len(attempted)}")

new_attempted = [c for c in attempted if c not in STUCK_CIDS]
with open(ORPHAN_FILE, 'w') as f:
    json.dump(new_attempted, f, indent=2)
print(f"After clear: {len(new_attempted)} entries")

# Now call redeem_positions_for_trade directly for each orphan
from crypto5min_polytrader.polymarket_redeem import redeem_positions_for_trade, _find_orphan_redeemable_positions

# Check what orphans are found
from crypto5min_polytrader.persistence import JsonStore
from pathlib import Path
TRADES_STORE = JsonStore(Path('logs') / 'poly_trades.json')
trades = TRADES_STORE.load(default=[]) or []
known_cids = {str(t.get('condition_id') or '').strip() for t in trades if t.get('condition_id')}
print(f"\nKnown condition IDs in trades log: {len(known_cids)}")

orphans = _find_orphan_redeemable_positions(known_cids)
print(f"Orphans found by scanner: {len(orphans)}")
for o in orphans:
    print(f"  cid={o['condition_id'][:20]}... value={o['current_value']} market={o['market'][:40]}")

print("\n--- Calling redeem_positions_for_trade directly for each orphan ---")
for cid in STUCK_CIDS:
    print(f"\nCID: {cid[:20]}...")
    try:
        res = redeem_positions_for_trade(
            trade={'condition_id': cid},
            dry_run=False,
        )
        print(f"  Result type: {type(res)}")
        print(f"  Result: {json.dumps(res, default=str)[:300]}")
    except Exception as e:
        import traceback
        print(f"  EXCEPTION: {e}")
        traceback.print_exc()

print("\nDone.")
