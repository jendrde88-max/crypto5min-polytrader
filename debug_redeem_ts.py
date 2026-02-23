#!/usr/bin/env python3
"""Debug redeem_submitted_ts values"""
import json, time

trades = json.load(open("logs/poly_trades.json"))
now = int(time.time())
print(f"now={now}")
drop_threshold = 600

for i, t in enumerate(trades):
    if t.get("redeem_status") == "submitted":
        raw = t.get("redeem_submitted_ts")
        print(f"\n--- Trade {i}: {t.get('question','?')[:50]}")
        print(f"  raw redeem_submitted_ts = {raw!r} (type={type(raw).__name__})")
        try:
            val = int(float(raw or 0))
        except:
            val = 0
        print(f"  parsed = {val}")
        print(f"  age = {now - val} sec ({(now-val)/3600:.1f} hrs)")
        print(f"  drop check: submitted_ts={bool(val)} and age>{drop_threshold} => {bool(val) and (now-val)>drop_threshold}")
