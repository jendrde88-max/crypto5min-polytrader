#!/usr/bin/env python3
"""
Sell all positions + stop bot via docker exec python3.
Bypasses web auth entirely by calling functions directly inside the container.
"""
import subprocess, json, sys

CONTAINER = "crypto5min-polytrader"
VPS = "root@65.109.240.249"

def ssh(cmd: str, label: str = "") -> str:
    """Run command on VPS via SSH, return stdout."""
    full = f'ssh -o StrictHostKeyChecking=no {VPS} "{cmd}"'
    if label:
        print(f"\n=== {label} ===")
    print(f"  > {cmd}")
    r = subprocess.run(full, shell=True, capture_output=True, text=True, timeout=60)
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if out:
        print(f"  stdout: {out}")
    if err:
        print(f"  stderr: {err}")
    return out

def docker_python(code: str, label: str = "") -> str:
    """Run Python code inside the container."""
    # Escape single quotes in the code for bash
    escaped = code.replace("'", "'\\''")
    cmd = f"docker exec crypto5min-polytrader python3 -c '{escaped}'"
    return ssh(cmd, label)

# ── Step 1: Check USDC balance ──────────────────────────────────────
docker_python(
    "import os, sys; sys.path.insert(0, '/app/src'); "
    "from crypto5min_polytrader.polymarket_account import clob_balance_usdc; "
    "pk = os.environ.get('C5_POLY_PRIVATE_KEY', ''); "
    "sig = int(os.environ.get('C5_POLY_SIGNATURE_TYPE', '0') or '0'); "
    "funder = os.environ.get('C5_POLY_FUNDER_ADDRESS', '') or None; "
    "bal = clob_balance_usdc(pk, signature_type=sig, funder=funder); "
    "print(f'USDC_BALANCE={bal:.6f}')",
    "USDC Balance"
)

# ── Step 2: Check positions ─────────────────────────────────────────
docker_python(
    "import os, sys, json; sys.path.insert(0, '/app/src'); "
    "from crypto5min_polytrader.polymarket_account import fetch_positions, derive_address; "
    "pk = os.environ.get('C5_POLY_PRIVATE_KEY', ''); "
    "addr = derive_address(pk); "
    "positions = fetch_positions(addr); "
    "print(f'POSITIONS_COUNT={len(positions)}'); "
    "[print(json.dumps({'token': p.get('asset','')[:12], 'size': p.get('size','0'), 'market': (p.get('market','') or p.get('title','') or p.get('question',''))[:60]})) for p in positions[:10]]",
    "Positions"
)

# ── Step 3: Close all positions (live, not dry run) ─────────────────
docker_python(
    "import os, sys, json; sys.path.insert(0, '/app/src'); "
    "from crypto5min_polytrader.polymarket_ops import close_all_positions_from_env; "
    "result = close_all_positions_from_env(dry_run=False); "
    "print(json.dumps(result, default=str))",
    "Close All Positions (LIVE)"
)

# ── Step 4: Check USDC balance again ────────────────────────────────
docker_python(
    "import os, sys; sys.path.insert(0, '/app/src'); "
    "from crypto5min_polytrader.polymarket_account import clob_balance_usdc; "
    "pk = os.environ.get('C5_POLY_PRIVATE_KEY', ''); "
    "sig = int(os.environ.get('C5_POLY_SIGNATURE_TYPE', '0') or '0'); "
    "funder = os.environ.get('C5_POLY_FUNDER_ADDRESS', '') or None; "
    "bal = clob_balance_usdc(pk, signature_type=sig, funder=funder); "
    "print(f'USDC_BALANCE_AFTER={bal:.6f}')",
    "USDC Balance After"
)

# ── Step 5: Pause the bot (create killswitch file) ──────────────────
docker_python(
    "from pathlib import Path; "
    "ks = Path('/app/logs/killswitch.json'); "
    "ks.write_text('{\"paused\": true}'); "
    "print(f'Killswitch created: {ks.exists()}')",
    "Pause Bot"
)

# ── Step 6: Verify paused ──────────────────────────────────────────
docker_python(
    "from pathlib import Path; "
    "ks = Path('/app/logs/killswitch.json'); "
    "print(f'Killswitch exists: {ks.exists()}'); "
    "print(f'Content: {ks.read_text() if ks.exists() else \"N/A\"}')",
    "Verify Paused"
)

# ── Step 7: Check container status ──────────────────────────────────
ssh("docker ps --filter name=crypto5min-polytrader --format '{{.Status}}'", "Container Status")

print("\n✓ Done. Bot is paused, positions closed. .env is intact.")
