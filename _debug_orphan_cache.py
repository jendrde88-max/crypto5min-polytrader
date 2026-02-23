"""Debug: check orphan cache vs data-api positions."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crypto5min_polytrader.polymarket_redeem import _load_orphan_attempted
from crypto5min_polytrader.polymarket_account import derive_address, fetch_positions

attempted = _load_orphan_attempted()
print(f"Cache entries: {len(attempted)}")
for a in attempted:
    print(f"  cached: {a[:20]}... len={len(a)}")

pk = os.getenv("C5_POLY_PRIVATE_KEY", "")
if pk:
    addr = derive_address(pk)
    positions = fetch_positions(addr)
    known_cids = set()  # empty for this debug — pretend no trades

    for p in positions:
        r = bool(p.get("redeemable"))
        try:
            cp = float(p.get("curPrice", 0))
        except:
            cp = 0.0
        try:
            v = float(p.get("currentValue", 0))
        except:
            v = 0.0
        if (r or cp >= 0.999) and v >= 0.01:
            cid = str(p.get("conditionId") or p.get("condition_id") or "").strip()
            in_cache = cid in attempted
            print(f"  candidate: cid={cid[:20]}... val=${v:.2f} in_cache={in_cache} len={len(cid)}")
else:
    print("No private key set")
