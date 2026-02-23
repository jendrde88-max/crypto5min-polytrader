#!/usr/bin/env python3
"""One-shot script to fix runtime_config.json settings.

Run inside the container:
  docker exec crypto5min-polytrader python3 /app/tools/fix_runtime_config.py
"""
import json

path = "/app/logs/runtime_config.json"
with open(path) as f:
    cfg = json.load(f)

print("BEFORE:")
print(json.dumps(cfg, indent=2))

# ── Fix dangerous settings ──────────────────────────────────────────
cfg["C5_CONFIDENCE_THRESHOLD"] = 0.55       # was 0.5  → coin-flip trades
cfg["C5_POLY_EDGE_MIN"]       = 0.03        # was 0.0  → edge gate disabled
cfg["C5_POLY_HIGH_RISK_MODE"] = "false"     # was true  → unrestricted risk
cfg["C5_POLY_BET_PERCENT"]    = 15.0        # was 30.0 → too aggressive
cfg["C5_RISK_CONSEC_LOSS_LIMIT"] = 5        # was 0    → no loss limit
cfg["C5_RISK_DAILY_LOSS_PCT"] = 25.0        # was 100  → no daily limit

with open(path, "w") as f:
    json.dump(cfg, f, indent=2)

print("\nAFTER:")
print(json.dumps(cfg, indent=2))
print("\n✓ runtime_config.json updated — changes take effect next trade cycle.")
