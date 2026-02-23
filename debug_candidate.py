import sys, os, json, time
sys.path.insert(0, '/app/src')

with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from crypto5min_polytrader.polymarket_redeem import select_redeem_candidates_from_trades

trades = json.load(open('/app/logs/poly_trades.json'))
now_ts = int(time.time())

candidates = select_redeem_candidates_from_trades(trades, max_trades=50, now=now_ts, retry_sec=60)
print(f"Candidates: {len(candidates)}")
for c in candidates:
    print(f"\nCandidate keys: {sorted(c.keys())}")
    print(f"trade_index: {c.get('trade_index', 'MISSING')}")
    print(f"order_status: {c.get('order_status')}")
    print(f"window_slug: {c.get('window_slug')}")
    print(f"question: {c.get('question')}")
    print(f"usdc: {c.get('usdc')}")
    print(f"condition_id: {c.get('condition_id')}")

# Also show what the SOL trade entry looks like directly
print("\n--- SOL trade from trades list ---")
sol_trades = [t for t in trades if 'sol' in (t.get('window_slug','') or '').lower()]
for t in sol_trades[-3:]:
    print(f"\n  Keys: {sorted(t.keys())}")
    print(f"  trade_index in list: {trades.index(t)}")
    print(f"  order_status: {t.get('order_status')}")
    print(f"  usdc: {t.get('usdc')}")
    print(f"  last_reconciled_ts: {t.get('last_reconciled_ts')}")
