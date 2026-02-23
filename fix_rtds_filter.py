"""Fix Chainlink RTDS SUBSCRIBE_MSG filter for v0.5.1.

Polymarket changed their RTDS WebSocket API behavior:
- Filtered subscriptions (e.g., {'symbol': 'btc/usd'}) now return
  a batch format with no streaming updates.
- Empty filter ('') returns proper individual streaming updates
  with topic/symbol/value fields.

This script changes the filter from json.dumps({'symbol': 'btc/usd'})
to '' (empty string) so the bot receives real-time price updates.

The v0.5.1 parser already filters client-side for 'btc/usd', so
receiving all assets is correctly handled.
"""
import pathlib
import sys

# Paths to fix
PATHS = [
    pathlib.Path('/root/crypto5min-polytrader/src/crypto5min_polytrader/chainlink_feed.py'),
    pathlib.Path('/app/src/crypto5min_polytrader/chainlink_feed.py'),  # inside container
]

OLD = "json.dumps({'symbol': 'btc/usd'})"
NEW = "''"

for p in PATHS:
    label = 'CONTAINER' if '/app/' in str(p) else 'HOST'
    if not p.exists():
        print(f'{label}: {p} not found (skip)')
        continue
    t = p.read_text()
    if OLD in t:
        t = t.replace(OLD, NEW)
        p.write_text(t)
        print(f'{label}: FIXED filters line')
    elif "'filters': ''" in t:
        print(f'{label}: Already fixed')
    else:
        print(f'{label}: WARNING - old string not found and not already fixed')

    # Show relevant lines
    for i, line in enumerate(t.splitlines(), 1):
        if 38 <= i <= 48:
            print(f'  {i}: {line}')
    print()
