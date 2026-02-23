#!/usr/bin/env python3
import json

data = json.load(open("/tmp/positions.json"))
nonzero = [p for p in data if float(p.get("currentValue", 0)) > 0.01]
print("=== Positions with value ===")
for p in nonzero:
    slug = p.get("slug", "?")
    val = p.get("currentValue", 0)
    size = p.get("size", 0)
    outcome = p.get("outcome", "?")
    initial = p.get("initialValue", 0)
    cur_price = p.get("curPrice", 0)
    redeemable = p.get("redeemable", False)
    title = p.get("title", "?")
    end_date = p.get("endDate", "?")
    print(f"  {slug}")
    print(f"    title: {title}")
    print(f"    outcome: {outcome} | endDate: {end_date}")
    print(f"    size: {size} | curPrice: {cur_price}")
    print(f"    initial: {initial} | current: {val}")
    print(f"    redeemable: {redeemable}")
    print()

# Unique slugs
slugs = set(p.get("slug", "?") for p in data)
print(f"Unique slugs: {len(slugs)}")

# Non-btc positions
non_btc = [p for p in data if not p.get("slug", "").startswith("btc-updown")]
print(f"\nNon-BTC positions: {len(non_btc)}")
for p in non_btc:
    slug = p.get("slug", "?")
    val = p.get("currentValue", 0)
    size = p.get("size", 0)
    outcome = p.get("outcome", "?")
    initial = p.get("initialValue", 0)
    redeemable = p.get("redeemable", False)
    print(f"  {slug} outcome={outcome} size={size} initial={initial} current={val} redeemable={redeemable}")

# BTC positions with non-zero value
btc_nonzero = [p for p in data if p.get("slug", "").startswith("btc-updown") and float(p.get("currentValue", 0)) > 0.01]
print(f"\nBTC positions with value: {len(btc_nonzero)}")
for p in btc_nonzero:
    slug = p.get("slug", "?")
    val = p.get("currentValue", 0)
    size = p.get("size", 0)
    outcome = p.get("outcome", "?")
    cur_price = p.get("curPrice", 0)
    redeemable = p.get("redeemable", False)
    print(f"  {slug} outcome={outcome} size={size} curPrice={cur_price} current={val} redeemable={redeemable}")

# Check total: are there positions not in our trade log?
print(f"\nTotal positions from API: {len(data)}")
print(f"Total in our trade log: 284")
btc_positions = [p for p in data if p.get("slug", "").startswith("btc-updown")]
print(f"BTC positions from API: {len(btc_positions)}")
