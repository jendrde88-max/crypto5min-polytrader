"""Analyze bot state to understand why it's not trading."""
import json
s = json.load(open("/app/logs/state.json"))
print("=== KEY STATE ===")
print("status:", s.get("status"))
print("poly_enabled:", s.get("poly_enabled"))
print("poly_dry_run:", s.get("poly_dry_run"))
print("usdc_balance:", s.get("usdc_balance"))
print("wallet:", s.get("wallet"))
print("last_trade_ts:", s.get("last_trade_ts"))
print("snipe_enabled:", s.get("snipe_enabled"))

mi = s.get("model_info") or {}
print("\n=== MODEL ===")
print("model status:", mi.get("status"))
print("confidence:", mi.get("confidence"))
print("direction:", mi.get("direction"))
print("threshold:", mi.get("threshold"))

print("\n=== TRADE-RELATED KEYS ===")
for k, v in sorted(s.items()):
    kl = k.lower()
    if any(x in kl for x in ["trade", "snipe", "cadence", "confidence", "gate", "skip", "window", "error", "last_"]):
        if not isinstance(v, (list, dict)) or len(str(v)) < 200:
            print(f"  {k}: {v}")
