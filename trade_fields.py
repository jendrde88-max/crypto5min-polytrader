import json
with open('/app/logs/poly_trades.json') as f:
    trades = json.load(f)
print('Keys:', list(trades[-1].keys()))
print('Last trade:', trades[-1])
