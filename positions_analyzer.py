#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
print(f"Total positions: {len(data)}")
redeemable = [p for p in data if p.get("redeemable")]
print(f"Redeemable: {len(redeemable)}")

nonzero = [p for p in data if float(p.get("currentValue", 0)) > 0.01]
print(f"Non-zero current value: {len(nonzero)}")
for p in nonzero:
    slug = p.get("slug", "?")
    val = p.get("currentValue", 0)
    size = p.get("size", 0)
    outcome = p.get("outcome", "?")
    print(f"  {slug} val={val} size={size} outcome={outcome}")

total_val = sum(float(p.get("currentValue", 0)) for p in data)
print(f"\nTotal currentValue sum: {total_val:.2f}")
total_initial = sum(float(p.get("initialValue", 0)) for p in data)
print(f"Total initialValue sum: {total_initial:.2f}")
total_cash_pnl = sum(float(p.get("cashPnl", 0)) for p in data)
print(f"Total cashPnl sum: {total_cash_pnl:.2f}")

# Sizes of redeemable
print(f"\nRedeemable sizes total: {sum(float(p.get('size', 0)) for p in redeemable):.2f}")
print(f"Redeemable positions: {len(redeemable)}")
for p in redeemable[:5]:
    slug = p.get("slug", "?")
    val = p.get("currentValue", 0)
    size = p.get("size", 0)
    outcome = p.get("outcome", "?")
    print(f"  {slug} val={val} size={size} outcome={outcome}")
