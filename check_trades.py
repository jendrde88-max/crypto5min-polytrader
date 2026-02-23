#!/usr/bin/env python3
"""Quick script to dump trade resolution statuses."""
import json, sys

trades = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'logs/poly_trades.json'))
for t in trades:
    slug = (t.get('window_slug') or '?')[-14:]
    d = t.get('direction', '?')
    usdc = t.get('usdc', 0)
    res = t.get('resolved', '-')
    os_ = t.get('order_status', '-')
    rs = t.get('redeem_status', '-')
    print(f"{slug:>14}  {d:>5}  ${usdc:>7.2f}  resolved={res:<14}  order={os_:<12}  redeem={rs}")
