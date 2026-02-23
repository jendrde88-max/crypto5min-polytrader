"""
Run auto-redeem dry-run first, then redeem for real if there are candidates.
Uses the container's live env and polymarket_redeem module.
"""
import sys, os
sys.path.insert(0, '/app/src')

# Load .env into environment
with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from crypto5min_polytrader.polymarket_redeem import process_auto_redeem

print("=" * 60)
print("STEP 1: Dry-run scan (no transactions)")
print("=" * 60)
dry = process_auto_redeem(dry_run=True)

skipped = dry.get('skipped', False)
if skipped:
    reason = dry.get('reason', '')
    print(f"Skipped: {reason}")
else:
    all_res = dry.get('results', []) + dry.get('orphan_results', [])
    print(f"Candidates found: {len(all_res)}")
    for r in all_res:
        slug = r.get('window_slug', r.get('condition_id', '')[:20])
        market = r.get('market', '')[:50]
        val = r.get('current_value', r.get('estimated_usdc', 0))
        orphan = ' [orphan]' if r.get('orphan') else ''
        print(f"  {slug}{orphan}  ~${float(val or 0):.2f}  ok={r.get('ok')}  {market}")

    if not all_res:
        print("Nothing to redeem right now.")
    else:
        print()
        print("=" * 60)
        print("STEP 2: LIVE REDEEM (real transactions)")
        print("=" * 60)
        result = process_auto_redeem(dry_run=False)
        live_res = result.get('results', []) + result.get('orphan_results', [])
        for r in live_res:
            slug = r.get('window_slug', r.get('condition_id', '')[:20])
            tx = r.get('tx_hash', r.get('relay_tx_id', ''))[:20] if (r.get('tx_hash') or r.get('relay_tx_id')) else 'no-tx'
            val = r.get('current_value', r.get('estimated_usdc', 0))
            orphan = ' [orphan]' if r.get('orphan') else ''
            status = 'OK' if r.get('ok') else f"FAIL: {r.get('error','?')}"
            print(f"  {status}  {slug}{orphan}  ~${float(val or 0):.2f}  tx={tx}")
        print(f"\nTotal processed: {len(live_res)}")
