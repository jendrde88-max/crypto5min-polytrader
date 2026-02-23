"""Quick bot status check — run inside the container."""
import json, time, os

trades_path = "/app/logs/poly_trades.json"
if not os.path.exists(trades_path):
    print("No trades file found")
    exit(1)

trades = json.load(open(trades_path))
now = time.time()

print(f"Total: {len(trades)} trades")

recent_2h = [t for t in trades if now - t.get("placed_ts", 0) < 7200]
recent_1h = [t for t in trades if now - t.get("placed_ts", 0) < 3600]
print(f"Last 1h: {len(recent_1h)}, Last 2h: {len(recent_2h)}")

if trades:
    last = trades[-1]
    age = int(now - last.get("placed_ts", 0))
    print(f"\nLast trade: {last.get('window_slug', '?')}")
    print(f"  direction={last.get('direction')} resolution={last.get('resolution')} status={last.get('order_status')}")
    print(f"  filled_size=${last.get('filled_size', 0):.2f} placed {age}s ago ({age // 60}min)")

# Count resolutions
res_counts = {}
for t in trades[-50:]:
    r = t.get("resolution", "?")
    res_counts[r] = res_counts.get(r, 0) + 1
print(f"\nLast 50 resolutions: {res_counts}")

# Check for pending
pending = [t for t in trades if t.get("resolution") == "pending"]
print(f"Pending trades: {len(pending)}")
for p in pending[-5:]:
    age = int(now - p.get("placed_ts", 0))
    print(f"  {p.get('window_slug', '?')[:50]} ({age}s / {age//60}min ago)")
