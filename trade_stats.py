import json, collections

with open('/app/logs/poly_trades.json') as f:
    trades = json.load(f)

resolved = [t for t in trades if t.get('resolved')]
wins = [t for t in resolved if t['resolved'] in ('win', 'win_unfilled')]
losses = [t for t in resolved if t['resolved'] in ('loss', 'loss_expired')]
pending = [t for t in trades if not t.get('resolved')]
sizes = [t.get('size', 0) for t in resolved]

print('Total trades:', len(trades))
print('Resolved:', len(resolved))
print('Wins:', len(wins), ' Losses:', len(losses))
print('Win rate:', round(len(wins) / max(1, len(resolved)) * 100, 1), '%')
print('Pending/open:', len(pending))
print('Avg bet size: $', round(sum(sizes) / max(1, len(sizes)), 2))

by_ticker = collections.Counter(t.get('ticker', '?') for t in resolved)
print('By ticker:', dict(sorted(by_ticker.items())))

today = [t for t in resolved if str(t.get('timestamp', '')).startswith('2026-02-21')]
today_wins = [t for t in today if t['resolved'] in ('win', 'win_unfilled')]
today_losses = [t for t in today if t['resolved'] in ('loss', 'loss_expired')]
print('Today - Wins:', len(today_wins), ' Losses:', len(today_losses))

# Win rate by confidence bucket
by_conf = [(t.get('confidence', 0), t['resolved']) for t in resolved]
buckets = {
    '<55%': {'w': 0, 'l': 0},
    '55-65%': {'w': 0, 'l': 0},
    '65-75%': {'w': 0, 'l': 0},
    '75-85%': {'w': 0, 'l': 0},
    '85%+': {'w': 0, 'l': 0},
}
for c, r in by_conf:
    if c < 0.55:
        k = '<55%'
    elif c < 0.65:
        k = '55-65%'
    elif c < 0.75:
        k = '65-75%'
    elif c < 0.85:
        k = '75-85%'
    else:
        k = '85%+'
    buckets[k]['w' if r in ('win', 'win_unfilled') else 'l'] += 1

print('\nWin rate by confidence bucket:')
for b, v in buckets.items():
    tot = v['w'] + v['l']
    if tot:
        print(f'  conf {b}: {v["w"]}W / {v["l"]}L = {round(v["w"]/tot*100)}%  (n={tot})')

# Last 20 trades
print('\nLast 10 trades:')
recent = sorted(trades, key=lambda t: t.get('timestamp', ''), reverse=True)[:10]
for t in recent:
    print(f"  {t.get('timestamp','?')[:16]}  {t.get('ticker','?'):4}  {t.get('direction','?'):4}  conf={t.get('confidence',0):.0%}  size=${t.get('size',0):.2f}  price={t.get('price',0):.2f}  resolved={t.get('resolved','pending')}")
