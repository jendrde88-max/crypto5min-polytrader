#!/usr/bin/env python3
"""Redeem resolved positions + verify final balance via paramiko SSH."""
import paramiko, json, sys

VPS = "65.109.240.249"
CONTAINER = "crypto5min-polytrader"

def ssh_cmd(cmd: str, label: str = "") -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(VPS, username="root")
    if label:
        print(f"\n=== {label} ===")
    print(f"  > {cmd[:120]}...")
    _, stdout, stderr = client.exec_command(cmd, timeout=60)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    client.close()
    if out:
        print(f"  {out}")
    if err and "WARNING" not in err.upper():
        print(f"  stderr: {err}")
    return out

def docker_py(code: str, label: str = "") -> str:
    # Write code to a temp file inside container, then execute it
    # This avoids all quoting issues
    escaped = code.replace("\\", "\\\\").replace('"', '\\"').replace('$', '\\$')
    write_cmd = f'docker exec {CONTAINER} bash -c "echo \\"{escaped}\\" > /tmp/_run.py"'
    ssh_cmd(write_cmd)
    return ssh_cmd(f"docker exec {CONTAINER} python3 /tmp/_run.py", label)


# ── Step 1: Dry-run redeem ──────────────────────────────────────────
docker_py(
    "import sys, json\\n"
    "sys.path.insert(0, '/app/src')\\n"
    "from crypto5min_polytrader.polymarket_redeem import process_auto_redeem\\n"
    "r = process_auto_redeem(dry_run=True)\\n"
    "print(json.dumps(r, default=str, indent=2))",
    "Redeem Dry Run"
)

# ── Step 2: Live redeem ─────────────────────────────────────────────
docker_py(
    "import sys, json\\n"
    "sys.path.insert(0, '/app/src')\\n"
    "from crypto5min_polytrader.polymarket_redeem import process_auto_redeem\\n"
    "r = process_auto_redeem(dry_run=False)\\n"
    "print(json.dumps(r, default=str, indent=2))",
    "Redeem LIVE"
)

# ── Step 3: Final USDC balance ──────────────────────────────────────
docker_py(
    "import os, sys\\n"
    "sys.path.insert(0, '/app/src')\\n"
    "from crypto5min_polytrader.polymarket_account import clob_balance_usdc\\n"
    "pk = os.environ.get('C5_POLY_PRIVATE_KEY', '')\\n"
    "sig = int(os.environ.get('C5_POLY_SIGNATURE_TYPE', '0') or '0')\\n"
    "funder = os.environ.get('C5_POLY_FUNDER_ADDRESS', '') or None\\n"
    "bal = clob_balance_usdc(pk, signature_type=sig, funder=funder)\\n"
    "print(f'FINAL_USDC_BALANCE={bal:.6f}')",
    "Final USDC Balance"
)

# ── Step 4: Verify killswitch still active ──────────────────────────
ssh_cmd(
    f"docker exec {CONTAINER} python3 -c 'from pathlib import Path; print(Path(\"/app/logs/killswitch.json\").exists())'",
    "Killswitch Check"
)

print("\n✓ Done.")
