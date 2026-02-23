import json
import time

trades = json.load(open('logs/poly_trades_remote.json'))

# Check usdc field and size field for actual bet amounts
usdc_vals = [t.get('usdc', 0) for t in trades]
size_vals = [t.get('size', 0) for t in trades]
print(f'usdc field: total={sum(usdc_vals):.2f}, non-zero={sum(1 for v in usdc_vals if v > 0)}')
print(f'size field: total={sum(size_vals):.2f}, non-zero={sum(1 for v in size_vals if v > 0)}')

# Check unfilled trades specifically
print('\n=== win_unfilled trades ===')
for t in trades:
    if t.get('resolved') == 'win_unfilled':
        resp = t.get('response', {})
        status = resp.get('status', '') if isinstance(resp, dict) else ''
        print(f"  slug={t.get('window_slug','?')} dir={t.get('direction','?')} order_status={t.get('order_status','?')} resp_status={status} price={t.get('price',0)} size={t.get('size',0)} usdc={t.get('usdc',0)}")

# Recent matched wins
print('\n=== Recent matched wins ===')
win_matched = [t for t in trades if t.get('resolved') == 'win' and isinstance(t.get('response', {}), dict) and t.get('response', {}).get('status') == 'matched']
for t in win_matched[-5:]:
    resp = t.get('response', {})
    print(f"  slug={t.get('window_slug','?')} making={resp.get('makingAmount',0)} taking={resp.get('takingAmount',0)} price={t.get('price',0)}")

# Last 10 trades
print('\n=== Last 10 trades ===')
for t in trades[-10:]:
    resp = t.get('response', {})
    status = resp.get('status', 'no_resp') if isinstance(resp, dict) else 'no_resp'
    ts = t.get('placed_ts', 0)
    dt = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts))
    print(f"  {dt} {t.get('direction','?'):>5} {t.get('order_status','?'):>20} resolved={t.get('resolved','?'):>15} resp={status:>10} price={t.get('price',0)} size={t.get('size',0)} usdc={t.get('usdc',0):.2f}")

# Money flow
print('\n=== Money Flow ===')
win_trades = [t for t in trades if t.get('resolved') == 'win' and isinstance(t.get('response', {}), dict) and t.get('response', {}).get('status') == 'matched']
loss_trades = [t for t in trades if t.get('resolved') == 'loss' and isinstance(t.get('response', {}), dict) and t.get('response', {}).get('status') == 'matched']

win_profit = sum(float(t['response']['takingAmount']) - float(t['response']['makingAmount']) for t in win_trades)
loss_amount = sum(float(t['response']['makingAmount']) for t in loss_trades)

print(f'Win profit (taking-making): {win_profit:.2f} from {len(win_trades)} wins')
print(f'Loss amount (making lost): {loss_amount:.2f} from {len(loss_trades)} losses')
print(f'Net P/L: {win_profit - loss_amount:.2f}')

total_making = sum(float(t.get('response', {}).get('makingAmount', 0)) for t in trades if isinstance(t.get('response', {}), dict) and t.get('response', {}).get('status') == 'matched')
print(f'Total USDC risked (all makingAmount): {total_making:.2f}')

# Recent wins that might be unredeemed
print('\n=== Recent wins (potential $12.65 source) ===')
recent_wins = [t for t in trades[-30:] if t.get('resolved') == 'win' and isinstance(t.get('response', {}), dict) and t.get('response', {}).get('status') == 'matched']
total_unredeemed = 0
for t in recent_wins:
    resp = t.get('response', {})
    taking = float(resp.get('takingAmount', 0))
    making = float(resp.get('makingAmount', 0))
    ts = t.get('placed_ts', 0)
    dt = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts))
    total_unredeemed += taking
    print(f"  {dt} {t.get('window_slug','?')} cost={making:.2f} shares={taking:.2f}")
print(f'  Total recent win shares: {total_unredeemed:.2f}')
