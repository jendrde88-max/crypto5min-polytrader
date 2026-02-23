"""
Force settlement detection + redeem cycle.
Runs process_resolved_trades (detects outcomes) then process_auto_redeem (claims).
"""
import sys, os, json, time
sys.path.insert(0, '/app/src')

with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from crypto5min_polytrader.polymarket_settlement import process_resolved_trades
from crypto5min_polytrader.polymarket_redeem import process_auto_redeem

print("=" * 60)
print("STEP 1: Detect resolved outcomes")
print("=" * 60)
settle = process_resolved_trades(dry_run=False)
print(f"Result: {json.dumps(settle, indent=2, default=str)[:2000]}")

print()
print("=" * 60)
print("STEP 2: Redeem won positions")
print("=" * 60)
dry = process_auto_redeem(dry_run=True)
skipped = dry.get('skipped', False)
if skipped:
    print(f"Dry-run: Skipped ({dry.get('reason')})")
else:
    all_res = dry.get('results', []) + dry.get('orphan_results', [])
    if not all_res:
        print("Dry-run: Nothing to redeem")
    else:
        print(f"Dry-run: {len(all_res)} candidate(s) found!")
        for r in all_res:
            slug = r.get('window_slug', (r.get('condition_id',''))[:20])
            val = r.get('current_value', r.get('estimated_usdc', 0))
            print(f"  {slug}  ~${float(val or 0):.2f}  ok={r.get('ok')}")
        
        print()
        print("=" * 60)
        print("STEP 3: LIVE REDEEM")
        print("=" * 60)
        result = process_auto_redeem(dry_run=False)
        live_res = result.get('results', []) + result.get('orphan_results', [])
        print(f"Redeemed: {len(live_res)}")
        for r in live_res:
            slug = r.get('window_slug', (r.get('condition_id',''))[:20])
            tx = (r.get('tx_hash', r.get('relay_tx_id','')) or '')[:20]
            status = 'OK' if r.get('ok') else f"FAIL: {r.get('error','?')}"
            print(f"  {status}  {slug}  tx={tx if tx else 'no-tx'}")
