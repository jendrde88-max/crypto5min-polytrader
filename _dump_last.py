import json
t = json.load(open("/app/logs/poly_trades.json"))[-1]
print(json.dumps(t, indent=2))
# Also check a filled trade
trades = json.load(open("/app/logs/poly_trades.json"))
filled = [x for x in trades if x.get("order_status") == "filled"]
if filled:
    print("\n--- LAST FILLED TRADE ---")
    print(json.dumps(filled[-1], indent=2))
