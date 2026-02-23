"""Check poly_trades.json for filled trades not yet redeemed, and their resolution status."""
import sys, os, json, time
from datetime import datetime, timezone

sys.path.insert(0, '/app/src')

with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

with open('/app/logs/poly_trades.json') as f:
    raw = json.load(f)

trades = raw if isinstance(raw, list) else list(raw.values()) if isinstance(raw, dict) else []
print(f"Total trades in log: {len(trades)}")

# Show all filled trades from the past 7 days
now = time.time()
recent = [t for t in trades if isinstance(t, dict) and float(t.get('placed_ts', 0)) > now - 7*86400]
recent.sort(key=lambda t: float(t.get('placed_ts', 0)))

print(f"Trades last 7 days: {len(recent)}")
print()

won = 0
lost = 0
pending = 0
already_redeemed = 0

for t in recent:
    ts = int(t.get('placed_ts', 0))
    dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%m/%d %H:%M UTC')
    q = t.get('question', t.get('window_slug', ''))[:55]
    direction = t.get('direction', '')
    conf = float(t.get('confidence', 0))
    usdc = float(t.get('usdc', t.get('intended_usdc', 0)) or 0)
    filled = float(t.get('filled_size', 0) or 0)
    status = t.get('order_status', '')
    resolved = t.get('resolved', 'pending')
    redeemed = t.get('redeemed', False)
    redeem_tx = t.get('redeem_tx_hash', t.get('relay_tx_id', ''))
    redeem_status = t.get('redeem_status', '')
    
    if status != 'filled':
        continue

    flag = ''
    if redeemed or redeem_status == 'success':
        already_redeemed += 1
        flag = '✓ REDEEMED'
    elif resolved == 'won' or (redeem_status and redeem_status not in ('error', '')):
        won += 1
        flag = f'WIN - {redeem_status or "pending_redeem"}'
    elif resolved == 'lost':
        lost += 1
        flag = 'LOST'
    else:
        pending += 1
        flag = f'unresolved ({resolved})'

    print(f"  {dt}  {direction:4} conf={conf:.0%}  ${usdc:.2f}→{filled:.1f}sh  [{flag}]  {q}")
    if redeem_tx:
        print(f"      redeem_tx={redeem_tx[:30]}")

print()
print(f"Summary: filled={len(recent)} | won+pending_redeem={won} | lost={lost} | redeemed={already_redeemed} | unresolved={pending}")

# Also check the orphan_redeemed.json to see what was already auto-redeemed
print()
print("=== orphan_redeemed.json ===")
try:
    with open('/app/logs/orphan_redeemed.json') as f:
        orp = json.load(f)
    print(json.dumps(orp, indent=2))
except Exception as e:
    print(f"  {e}")
