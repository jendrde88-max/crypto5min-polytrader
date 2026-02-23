#!/usr/bin/env python3
"""Analyze poly_trades.json for missing redeems."""
import json, sys
from collections import Counter

trades = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "logs/poly_trades.json"))
print(f"Total trades: {len(trades)}")
print(f"Resolved: {dict(Counter(t.get('resolved','NONE') for t in trades))}")
print(f"Redeem: {dict(Counter(t.get('redeem_status','NONE') for t in trades))}")

wins = [t for t in trades if t.get("resolved") == "win"]
print(f"\nTotal wins: {len(wins)}")

unredeemed = [t for t in wins if t.get("redeem_status","") not in ("success","submitted")]
print(f"Unredeemed wins: {len(unredeemed)}")
for t in unredeemed[:20]:
    print(f"  Q: {t.get('question','?')[:65]}")
    print(f"    redeem_status={t.get('redeem_status','NONE')} filled={t.get('filled_size',0)} order_status={t.get('order_status')}")
    print(f"    condition_id={t.get('condition_id','?')}")

unresolved = [t for t in trades if not t.get("resolved")]
print(f"\nUnresolved trades: {len(unresolved)}")
for t in unresolved[:20]:
    print(f"  Q: {t.get('question','?')[:65]}")
    print(f"    order_status={t.get('order_status')} filled={t.get('filled_size',0)} cancel_reason={t.get('cancel_reason','')}")

# Check for trades resolved=win with filled_size > 0 but no redeem
filled_wins_no_redeem = [t for t in wins if (t.get("filled_size",0) or 0) > 0 and t.get("redeem_status","") not in ("success","submitted")]
print(f"\nFilled wins without redeem (MONEY LEFT ON TABLE): {len(filled_wins_no_redeem)}")
for t in filled_wins_no_redeem:
    print(f"  Q: {t.get('question','?')[:65]}")
    print(f"    filled={t.get('filled_size')} usdc={t.get('usdc')} redeem={t.get('redeem_status','NONE')}")
    print(f"    condition_id={t.get('condition_id')}")

# Check for trades with redeem_status=failed or error
failed_redeems = [t for t in trades if t.get("redeem_status","") in ("failed","error")]
print(f"\nFailed redeems: {len(failed_redeems)}")
for t in failed_redeems:
    print(f"  Q: {t.get('question','?')[:65]}")
    print(f"    redeem_status={t.get('redeem_status')} condition_id={t.get('condition_id')}")
    print(f"    redeem_tx_hash={t.get('redeem_tx_hash','NONE')}")
    print(f"    redeem_attempted_ts={t.get('redeem_attempted_ts','NONE')}")
    print(f"    filled_size={t.get('filled_size')} usdc={t.get('usdc')}")
    print(f"    settlement_result={t.get('settlement_result')}")
    
# Submitted but not confirmed redeems  
submitted = [t for t in trades if t.get("redeem_status") == "submitted"]
print(f"\nSubmitted but NOT confirmed redeems: {len(submitted)}")
for t in submitted:
    print(f"  Q: {t.get('question','?')[:65]}")
    print(f"    redeem_tx_hash={t.get('redeem_tx_hash','NONE')}")
    print(f"    redeem_submitted_ts={t.get('redeem_submitted_ts','NONE')}")
    print(f"    redeemed_ts={t.get('redeemed_ts','NONE')}")
    print(f"    resolved={t.get('resolved')} filled_size={t.get('filled_size')} usdc={t.get('usdc')}")
    print(f"    condition_id={t.get('condition_id')}")
    print(f"    settlement_result={t.get('settlement_result')}")
    print()

# Summary of money
total_usdc_wins = sum(t.get("usdc",0) for t in wins)
redeemed_wins = [t for t in wins if t.get("redeem_status") == "success"]
redeemed_usdc = sum(t.get("usdc",0) for t in redeemed_wins)
submitted_usdc = sum(t.get("usdc",0) for t in submitted)
error_usdc = sum(t.get("usdc",0) for t in failed_redeems)
print(f"\n=== MONEY SUMMARY ===")
print(f"Total win USDC wagered: ${total_usdc_wins:.2f}")
print(f"Successfully redeemed: ${redeemed_usdc:.2f} ({len(redeemed_wins)} trades)")
print(f"Submitted/stuck redeems: ${submitted_usdc:.2f} ({len(submitted)} trades)")
print(f"Error redeems: ${error_usdc:.2f} ({len(failed_redeems)} trades)")
print(f"Total losses: ${sum(t.get('usdc',0) for t in trades if t.get('resolved')=='loss'):.2f} ({len([t for t in trades if t.get('resolved')=='loss'])} trades)")

# Print tx hashes for on-chain verification
print("\n=== TX HASHES TO VERIFY ON-CHAIN ===")
for t in submitted:
    print(t.get("redeem_tx_hash","NONE"))
print()
if failed_redeems:
    print("Error redeem condition_ids to retry:")
    for t in failed_redeems:
        print(f"  {t.get('condition_id')}")
        
# Check what open positions look like
open_pos = [t for t in trades if t.get("resolved") == "win" and t.get("redeem_status") in ("submitted","error")]
print(f"\nPositions that might still hold CTF tokens: {len(open_pos)}")
for t in open_pos:
    print(f"  condition={t.get('condition_id')}")
    print(f"  token_id={t.get('token_id')}")
    print(f"  usdc={t.get('usdc')}")
