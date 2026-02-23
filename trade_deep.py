import json, collections, time

with open('/app/logs/poly_trades.json') as f:
    trades = json.load(f)

# Fix: use placed_ts for date filtering
today_start = 1771632000  # Feb 21 2026 00:00 UTC approx
resolved = [t for t in trades if t.get('resolved')]

# Split by bet_mode / order type / snipe vs model
snipe = [t for t in resolved if t.get('bet_mode') == 'snipe' or t.get('order_type') == 'FOK']
model = [t for t in resolved if t not in snipe]

def stats(lst, label):
    if not lst:
        print(f'{label}: no trades')
        return
    wins = [t for t in lst if t['resolved'] in ('win', 'win_unfilled')]
    losses = [t for t in lst if t['resolved'] in ('loss', 'loss_expired')]
    n = len(lst)
    wr = len(wins)/n*100
    avg_price = sum(t.get('avg_fill_price', t.get('price', 0)) for t in lst)/n
    avg_conf = sum(t.get('confidence', 0) for t in lst)/n
    avg_size = sum(t.get('usdc', t.get('size', 0)) for t in lst)/n
    print(f'{label}: {n} trades  {len(wins)}W/{len(losses)}L = {wr:.1f}%  avg_conf={avg_conf:.1%}  avg_fill_price=${avg_price:.3f}  avg_usdc=${avg_size:.2f}')

stats(resolved, 'ALL')
stats(snipe, 'SNIPE')
stats(model, 'MODEL')

# By direction
for direction in ('UP', 'DOWN'):
    d = [t for t in resolved if t.get('direction') == direction]
    stats(d, f'  dir={direction}')

# Today trades (using placed_ts unix)
today_trades = [t for t in resolved if t.get('placed_ts', 0) >= today_start]
stats(today_trades, 'TODAY')

# Prices paid
print('\nPrice distribution (what price did we pay?):')
price_buckets = {'<0.30': 0, '0.30-0.50': 0, '0.50-0.70': 0, '0.70-0.85': 0, '0.85-0.95': 0, '>0.95': 0}
for t in resolved:
    p = t.get('avg_fill_price', t.get('price', 0))
    if p < 0.30: k = '<0.30'
    elif p < 0.50: k = '0.30-0.50'
    elif p < 0.70: k = '0.50-0.70'
    elif p < 0.85: k = '0.70-0.85'
    elif p < 0.95: k = '0.85-0.95'
    else: k = '>0.95'
    price_buckets[k] += 1
for b, c in price_buckets.items():
    print(f'  {b}: {c} trades')

# Questions (unique markets traded)
market_counts = collections.Counter(t.get('question', '')[:50] for t in resolved)
print('\nTop market types:')
for q, c in market_counts.most_common(10):
    print(f'  {c:3}x  {q}')

# Win rate by price bucket
print('\nWin rate by fill price:')
for b in ['<0.30', '0.30-0.50', '0.50-0.70', '0.70-0.85', '0.85-0.95', '>0.95']:
    bucket_trades = [t for t in resolved if True]
    sub = []
    for t in resolved:
        p = t.get('avg_fill_price', t.get('price', 0))
        if b == '<0.30' and p < 0.30: sub.append(t)
        elif b == '0.30-0.50' and 0.30 <= p < 0.50: sub.append(t)
        elif b == '0.50-0.70' and 0.50 <= p < 0.70: sub.append(t)
        elif b == '0.70-0.85' and 0.70 <= p < 0.85: sub.append(t)
        elif b == '0.85-0.95' and 0.85 <= p < 0.95: sub.append(t)
        elif b == '>0.95' and p >= 0.95: sub.append(t)
    if sub:
        w = sum(1 for t in sub if t['resolved'] in ('win', 'win_unfilled'))
        print(f'  price {b}: {w}W/{len(sub)-w}L = {w/len(sub)*100:.0f}%  (n={len(sub)})')
