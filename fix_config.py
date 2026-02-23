import json
with open('/app/logs/runtime_config.json') as f:
    cfg = json.load(f)
cfg['C5_POLY_BET_PERCENT'] = 10.0
cfg['C5_POLY_HIGH_RISK_MODE'] = 'false'
cfg['C5_POLY_MAX_USDC_PER_TRADE'] = 100.0
cfg['C5_CONFIDENCE_THRESHOLD'] = 0.55
with open('/app/logs/runtime_config.json', 'w') as f:
    json.dump(cfg, f, indent=2)
print('DONE')
with open('/app/logs/runtime_config.json') as f:
    print(f.read())
