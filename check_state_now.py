"""Check chainlink-related fields in state.json."""
import json

with open('/app/logs/state.json') as f:
    d = json.load(f)

# Print all keys
print("=== ALL TOP-LEVEL KEYS ===")
for k in sorted(d.keys()):
    v = d[k]
    if isinstance(v, dict):
        print(f"  {k}: (dict with {len(v)} keys)")
    elif isinstance(v, list):
        print(f"  {k}: (list with {len(v)} items)")
    else:
        print(f"  {k}: {v}")

# Check for chainlink-related fields
print("\n=== CHAINLINK FIELDS ===")
for k in d:
    if 'chainlink' in k.lower() or 'oracle' in k.lower() or 'basis' in k.lower():
        print(f"  {k}: {d[k]}")

# Check nested dicts
for k in d:
    if isinstance(d[k], dict):
        for sk in d[k]:
            if 'chainlink' in sk.lower() or 'oracle' in sk.lower() or 'basis' in sk.lower() or 'price' in sk.lower() or 'source' in sk.lower():
                print(f"  {k}.{sk}: {d[k][sk]}")
