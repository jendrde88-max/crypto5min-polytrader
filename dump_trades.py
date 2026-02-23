import json
with open("/app/logs/poly_trades.json") as f:
    trades = json.load(f)
print(f"Total trades: {len(trades)}")
if trades:
    # Show last 3 trades with all keys
    for t in trades[-3:]:
        print(json.dumps(t, indent=2, default=str))
        print("---")
    # Show all unique keys across all trades
    all_keys = set()
    for t in trades:
        all_keys.update(t.keys())
    print(f"\nAll keys: {sorted(all_keys)}")
    # Count outcomes
    outcomes = {}
    for t in trades:
        o = t.get("outcome", "NONE")
        outcomes[o] = outcomes.get(o, 0) + 1
    print(f"\nOutcome distribution: {outcomes}")
    # Count order_status
    statuses = {}
    for t in trades:
        s = t.get("order_status", "NONE")
        statuses[s] = statuses.get(s, 0) + 1
    print(f"Order status distribution: {statuses}")
    # Count snipe field
    snipe_count = sum(1 for t in trades if t.get("snipe"))
    print(f"Snipe trades: {snipe_count}")
