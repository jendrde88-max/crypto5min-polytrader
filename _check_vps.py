#!/usr/bin/env python3
"""Check our VPS bot state and settings."""
import paramiko, json

HOST = "65.109.240.249"
USER = "root"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, timeout=10)

def run(cmd):
    _, out, err = ssh.exec_command(cmd, timeout=30)
    return out.read().decode().strip()

# State (condensed)
print("=== STATE ===")
raw = run("docker exec crypto5min-polytrader cat /app/logs/state.json 2>/dev/null")
if raw:
    s = json.loads(raw)
    condensed = {k: v for k, v in s.items() if k not in ('backtest', 'symbols', 'wallet', 'redeem', 'redeem_reconcile')}
    print(json.dumps(condensed, indent=2))

# Runtime config
print("\n=== RUNTIME CONFIG ===")
rc = run("docker exec crypto5min-polytrader cat /app/logs/runtime_config.json 2>/dev/null")
if rc:
    print(json.dumps(json.loads(rc), indent=2))

# .env key settings
print("\n=== .ENV SETTINGS ===")
env = run("docker exec crypto5min-polytrader cat /app/config/.env 2>/dev/null")
if env:
    for line in env.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key = line.split('=', 1)[0] if '=' in line else ''
        # Show non-secret config keys
        if any(k in key.upper() for k in ['DELTA', 'SNIPE', 'CONFIDENCE', 'KELLY', 'HIGH_RISK', 'BET_PERCENT', 'MODE', 'DRY', 'SYMBOL', 'ENABLED', 'ARB', 'EXPERT', 'FORCE_GTC', 'REDEEM', 'INCREMENT', 'RTDS']):
            print(line)

# Recent app log (last 40 lines)
print("\n=== RECENT LOG (last 40 lines) ===")
log = run("docker exec crypto5min-polytrader tail -40 /app/logs/app.log 2>/dev/null")
print(log)

# Docker stats
print("\n=== STATS ===")
stats = run("docker stats --no-stream crypto5min-polytrader --format 'CPU={{.CPUPerc}} MEM={{.MemUsage}}'")
print(stats)

# Version
print("\n=== VERSION ===")
ver = run("docker exec crypto5min-polytrader cat /app/VERSION 2>/dev/null")
print(ver)

ssh.close()
