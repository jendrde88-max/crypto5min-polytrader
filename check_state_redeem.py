#!/usr/bin/env python3
"""Quick script to dump redeem and redeem_reconcile from state.json."""
import json, sys

s = json.load(open('logs/state.json'))
for key in ('redeem', 'redeem_reconcile'):
    val = s.get(key)
    if val:
        print(f'\n=== {key} ===')
        print(json.dumps(val, indent=2))
    else:
        print(f'\n=== {key} === (not present)')
