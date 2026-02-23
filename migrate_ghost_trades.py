"""One-time migration: reclassify ghost trades (win→win_unfilled, loss→loss_unfilled)."""
import json

path = 'logs/poly_trades.json'
with open(path, 'r') as f:
    trades = json.load(f)

fixed = 0
for i, t in enumerate(trades):
    if not isinstance(t, dict):
        continue
    resolved = t.get('resolved', '')
    order_status = str(t.get('order_status') or '').strip().lower()
    resp = t.get('response') or {}
    taking = 0
    if isinstance(resp, dict):
        try:
            taking = float(resp.get('takingAmount') or 0)
        except Exception:
            pass
    filled_size = 0
    try:
        filled_size = float(t.get('filled_size') or 0)
    except Exception:
        pass

    is_filled = order_status in ('filled', 'matched') or taking > 0 or filled_size > 0

    if resolved == 'win' and not is_filled:
        t['resolved'] = 'win_unfilled'
        fixed += 1
        print(f'  Fixed [{i}] {t.get("window_slug","?")}: win -> win_unfilled (order_status={order_status})')
    elif resolved == 'loss' and not is_filled:
        t['resolved'] = 'loss_unfilled'
        fixed += 1
        print(f'  Fixed [{i}] {t.get("window_slug","?")}: loss -> loss_unfilled (order_status={order_status})')

if fixed > 0:
    with open(path, 'w') as f:
        json.dump(trades, f, indent=2)
    print(f'\nMigrated {fixed} ghost trades')
else:
    print('No ghost trades to migrate')

# Show new stats
wins = sum(1 for t in trades if t.get('resolved') == 'win')
losses = sum(1 for t in trades if t.get('resolved') == 'loss')
wu = sum(1 for t in trades if t.get('resolved') == 'win_unfilled')
lu = sum(1 for t in trades if t.get('resolved') == 'loss_unfilled')
total_filled = wins + losses
wr = (wins / total_filled * 100) if total_filled > 0 else 0
print(f'\nNew stats: {wins}W/{losses}L filled ({wr:.1f}%), {wu} ghost wins, {lu} ghost losses')
