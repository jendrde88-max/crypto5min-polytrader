"""Switch bet mode from kelly to percent inside the running container."""
import json

path = 'logs/runtime_config.json'
with open(path) as f:
    cfg = json.load(f)

cfg['C5_POLY_BET_MODE'] = 'percent'
cfg['C5_POLY_BET_PERCENT'] = 10.0

with open(path, 'w') as f:
    json.dump(cfg, f, indent=2)

print(f"Updated: BET_MODE={cfg['C5_POLY_BET_MODE']}, BET_PERCENT={cfg['C5_POLY_BET_PERCENT']}")
