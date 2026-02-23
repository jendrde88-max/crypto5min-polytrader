"""Debug 2: check if 0xed40e1 is in trades known_cids."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from crypto5min_polytrader.persistence import JsonStore
from pathlib import Path

trades = JsonStore(Path('logs') / 'poly_trades.json').load(default=[])
cids = set()
for t in trades:
    if not isinstance(t, dict):
        continue
    c = str(t.get('condition_id') or t.get('conditionId') or '').strip()
    if c:
        cids.add(c)
print(f"Total unique condition_ids in trades: {len(cids)}")
print(f"0xed40 in trades: {any('0xed40' in c for c in cids)}")

# Also check the auto-redeem flow
from crypto5min_polytrader.polymarket_redeem import _find_orphan_redeemable_positions
orphans = _find_orphan_redeemable_positions(cids)
print(f"Orphan candidates (after known_cids filter): {len(orphans)}")
for o in orphans:
    print(f"  {o['condition_id'][:20]}... val=${o['current_value']:.2f}")
