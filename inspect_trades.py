import json, os, glob

# Find all JSON files in logs
log_dir = '/app/logs'
for root, dirs, files in os.walk(log_dir):
    for f in files:
        if f.endswith('.json'):
            full = os.path.join(root, f)
            size = os.path.getsize(full)
            print(f'  {full} ({size} bytes)')

print()

# Show structure of last trade
tf = os.path.join(log_dir, 'poly_trades.json')
if os.path.exists(tf):
    data = json.load(open(tf))
    print(f'poly_trades.json: {len(data)} records')
    if data:
        last = data[-1]
        print('Last trade keys:', sorted(last.keys()))
        print('Last trade sample:')
        for k, v in sorted(last.items()):
            print(f'  {k}: {repr(v)[:80]}')
