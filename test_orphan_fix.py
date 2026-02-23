"""Manually trigger auto-redeem to test the orphan fix."""
import sys
sys.path.insert(0, '/app/src')
import os
from pathlib import Path

# Load .env so keys are available
from dotenv import load_dotenv
load_dotenv(Path('/app/.env'), override=True)

from crypto5min_polytrader.polymarket_redeem import (
    _load_orphan_attempted,
    _find_orphan_redeemable_positions,
    process_auto_redeem,
)
import json

print("=== Orphan attempted (after fix) ===")
attempted = _load_orphan_attempted()
print(f"  Blocked count: {len(attempted)}")
if attempted:
    for a in attempted:
        print(f"    {a}")
else:
    print("  (empty - all expired)")

print()
print("=== Orphan redeemable_positions ===")
known = set()
trades = json.loads(Path('/app/logs/poly_trades.json').read_text())
for t in trades:
    if isinstance(t, dict):
        cid = str(t.get('condition_id') or t.get('conditionId') or '').strip()
        if cid:
            known.add(cid)
print(f"  Known condition_ids from trades: {len(known)}")

orphans = _find_orphan_redeemable_positions(known)
print(f"  Orphan positions found: {len(orphans)}")
for o in orphans:
    print(f"    condition_id={o.get('condition_id','?')[:20]}... value=${o.get('current_value',0):.2f} market={o.get('market','?')[:50]}")

print()
print("=== Running process_auto_redeem (DRY RUN) ===")
result = process_auto_redeem(dry_run=True)
print(f"  result: {result}")
