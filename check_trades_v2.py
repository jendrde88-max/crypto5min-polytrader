import json, pathlib, time
from datetime import datetime, timezone

p = pathlib.Path('/app/logs/poly_trades_live.json')
if not p.exists():
    print('no poly_trades_live.json')
    exit()

trades = json.loads(p.read_text())
if isinstance(trades, list):
    all_trades = trades
elif isinstance(trades, dict):
    all_trades = list(trades.values())
else:
    print('unexpected format')
    exit()

now = time.time()
recent = [t for t in all_trades if isinstance(t, dict) and float(t.get('placed_ts', 0)) > now - 21600]
recent.sort(key=lambda x: float(x.get('placed_ts', 0)))

print(f"=== Last {len(recent)} trades (6h window) ===")
for t in recent[-15:]:
    ts = int(t.get('placed_ts', 0))
    dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%H:%M:%S')
    q = t.get('question', '')[:40]
    direction = t.get('direction', '')
    conf = float(t.get('confidence', 0))
    delta = float(t.get('delta_pct', 0) or 0)
    usdc = float(t.get('usdc', 0) or 0)
    status = t.get('order_status', '')
    resolved = t.get('resolved', 'pending')
    print(f"  {dt}UTC {direction:4} conf={conf:.0%} delta={delta:.3f}% {usdc:.2f}USDC {status:8} res={resolved:7} | {q}")

print()
if recent:
    last = recent[-1]
    print(f"Last position USDC: {last.get('usdc', 'N/A')}")
    print(f"Last placed_ts: {last.get('placed_ts', 'N/A')}")

print()
print("=== v0.7.2-dev field check (last 5) ===")
for t in recent[-5:]:
    keys = list(t.keys())
    has_rdp = 'recent_delta_pct' in t
    has_dp = 'delta_pct' in t
    print(f"  {t.get('window_slug','')[:28]} recent_delta_pct={has_rdp} delta_pct={has_dp}")
