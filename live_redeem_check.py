#!/usr/bin/env python3
import json

trades = json.load(open('logs/poly_trades_live.json'))
print(f'Total trades: {len(trades)}')

# Check btc-updown-5m-1771288200
for t in trades:
    if t.get('window_slug') == 'btc-updown-5m-1771288200':
        print('\nbtc-updown-5m-1771288200:')
        print(f"  resolved={t.get('resolved')} redeem_status={t.get('redeem_status', 'NONE')}")
        print(f"  redeem_tx_hash={t.get('redeem_tx_hash', 'NONE')}")
        print(f"  redeem_attempted_ts={t.get('redeem_attempted_ts', 'NONE')}")
        print(f"  order_status={t.get('order_status')}")

# Check wins without successful redeem
print('\n=== Wins without successful redeem ===')
for t in trades:
    if t.get('resolved') == 'win' and t.get('redeem_status') != 'success':
        slug = t.get('window_slug', '?')
        rdm = t.get('redeem_status', 'NONE')
        rdm_ts = t.get('redeem_attempted_ts', 'NONE')
        rdm_tx = t.get('redeem_tx_hash', 'NONE')
        err = t.get('redeem_error', '')
        os_ = t.get('order_status', '?')
        print(f"  {slug} order={os_} redeem={rdm} err={err} attempted={rdm_ts} tx={rdm_tx}")

# Last 3 trades
print('\n=== Last 3 trades ===')
for t in trades[-3:]:
    slug = t.get('window_slug', '?')
    rs = t.get('resolved', '?')
    rdm = t.get('redeem_status', 'NONE')
    os_ = t.get('order_status', '?')
    print(f"  {slug} resolved={rs} order={os_} redeem={rdm}")
