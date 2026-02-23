#!/usr/bin/env python3
"""
Force-redeem all 5 stuck positions:
 - 4 orphans blacklisted in orphan_redeemed.json (already_attempted cache)
 - 1 win_unfilled trade stuck in trades log

Strategy: clear the already_attempted cache for these, fix resolved field, then call process_auto_redeem.
"""
import sys, os, json, asyncio
sys.path.insert(0, '/app/src')

ORPHAN_FILE = '/app/logs/orphan_redeemed.json'
TRADES_FILE = '/app/logs/poly_trades.json'

# The 5 stuck condition IDs we need to force-redeem
STUCK_POSITIONS = {
    # orphans (in already_attempted list)
    "0x78e6508b6dcf4ca3f0419a6343bc2413bb6315cbbfc600af8dc05603aca75dd1": "ETH Down 12:55-1:00PM $5.00",
    "0x5d8e5293632061a2972ad1ddc84c5030fddb29f5f884e2f43ecd4509af55b499": "XRP Down 1:05-1:10PM $5.00",
    "0xc98e31d95733702687301fbb701ec462c0a64b46a8dfd5d8550b05785286b4b2": "Borussia Dortmund $2.21",
    "0x819b3f58db41c9cc097db7343906fe0c37f2f206b425a2aab1a40be2911c5ae3": "UC Sampdoria $1.89",
    # win_unfilled (in trades log with wrong resolved status)
    "0x72a360ae98df0f9b252022b388803dd1c7a73be4bf57765c87a8623eccc6ef69": "ETH Down 1:10-1:15PM $10.72",
}

print("=== FORCE REDEEM: 5 STUCK POSITIONS ===\n")

# Step 1: Clear stuck positions from orphan_redeemed.json cache
print("[1] Clearing already_attempted cache for stuck positions...")
try:
    with open(ORPHAN_FILE) as f:
        attempted = json.load(f)
    print(f"    Before: {len(attempted)} entries")
    new_attempted = [cid for cid in attempted if cid not in STUCK_POSITIONS]
    with open(ORPHAN_FILE, 'w') as f:
        json.dump(new_attempted, f, indent=2)
    print(f"    After:  {len(new_attempted)} entries (removed {len(attempted)-len(new_attempted)})")
except FileNotFoundError:
    print("    File not found - creating empty")
    with open(ORPHAN_FILE, 'w') as f:
        json.dump([], f)

# Step 2: Fix the win_unfilled trade - set resolved='win' so main loop picks it up
WIN_UNFILLED_CID = "0x72a360ae98df0f9b252022b388803dd1c7a73be4bf57765c87a8623eccc6ef69"
print(f"\n[2] Fixing win_unfilled trade (ETH $10.72)...")
try:
    with open(TRADES_FILE) as f:
        trades = json.load(f)
    fixed = False
    for t in trades:
        if t.get('condition_id') == WIN_UNFILLED_CID:
            old = t.get('resolved')
            if old == 'win_unfilled':
                t['resolved'] = 'win'
                t['order_status'] = 'filled'  # treat as filled so main loop processes it
                print(f"    Fixed: resolved {old} -> win, order_status -> filled")
                print(f"    Trade: {t.get('window_slug')} usdc={t.get('usdc')}")
                fixed = True
    if not fixed:
        print("    Trade not found or already fixed")
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=2)
    print("    Trades log saved.")
except Exception as e:
    print(f"    Error: {e}")

# Step 3: Run process_auto_redeem(dry_run=False) to trigger redemptions
print(f"\n[3] Running process_auto_redeem(dry_run=False)...")
try:
    from crypto5min_polytrader.polymarket_redeem import process_auto_redeem
    result = process_auto_redeem(dry_run=False)
    print(f"    status: {result.get('status')}")
    print(f"    message: {result.get('message')}")
    results = result.get('results', [])
    orphan_results = result.get('orphan_results', [])
    print(f"    trade results: {len(results)}")
    print(f"    orphan results: {len(orphan_results)}")
    
    for r in results + orphan_results:
        ok = r.get('ok') or r.get('result', {}).get('ok')
        tx = r.get('tx_hash') or r.get('result', {}).get('tx_hash', '')
        err = r.get('error') or r.get('result', {}).get('error', '')
        cid = r.get('condition_id', r.get('orphan', {}).get('condition_id', ''))
        name = STUCK_POSITIONS.get(cid, cid[:20]+'...')
        print(f"    {'✓' if ok else '✗'} {name} | tx={tx[:20] if tx else ''} err={err}")
        
except Exception as e:
    import traceback
    print(f"    Error: {e}")
    traceback.print_exc()

print("\n=== Done. Check dashboard for updated balance ===")
