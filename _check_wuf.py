import json, time

trades = json.load(open("/app/logs/poly_trades.json"))

slugs = ["btc-updown-5m-1771332300", "btc-updown-5m-1771331700"]
for slug in slugs:
    matches = [t for t in trades if t.get("window_slug") == slug]
    print(f"=== {slug} ({len(matches)} trade(s)) ===")
    for t in matches:
        print(json.dumps({k: t.get(k) for k in [
            "window_slug", "direction", "order_status", "filled_size",
            "resolved", "resolved_outcome", "resolved_ts",
            "redeem_status", "redeemed_ts", "redeem_tx_hash",
            "last_reconciled_ts", "placed_ts", "price", "usdc",
            "order_type", "fill_attempts", "cancel_reason",
            "condition_id", "response"
        ]}, indent=2))
    print()

# Also count how many win_unfilled in last 20 trades
last20 = trades[-20:]
wuf = [t for t in last20 if t.get("resolved") == "win_unfilled"]
canceled = [t for t in last20 if "canceled" in str(t.get("order_status", ""))]
filled = [t for t in last20 if t.get("order_status") == "filled"]
print(f"Last 20 trades: {len(filled)} filled, {len(canceled)} canceled, {len(wuf)} win_unfilled")

# Check if these have resolved field set
for slug in slugs:
    matches = [t for t in trades if t.get("window_slug") == slug]
    for t in matches:
        print(f"{slug}: resolved={t.get('resolved')}, order_status={t.get('order_status')}, filled={t.get('filled_size')}")
