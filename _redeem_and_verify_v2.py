#!/usr/bin/env python3
"""
Redeem resolved positions + verify final balance.
Uses paramiko to SSH, writes script to container via docker cp, then executes.
"""
import paramiko, json, sys, tempfile, os

VPS = "65.109.240.249"
CONTAINER = "crypto5min-polytrader"

REDEEM_SCRIPT = '''
import sys, os, json
sys.path.insert(0, '/app/src')

from crypto5min_polytrader.polymarket_redeem import process_auto_redeem
from crypto5min_polytrader.polymarket_account import clob_balance_usdc

# Check balance before
pk = os.environ.get('C5_POLY_PRIVATE_KEY', '')
sig = int(os.environ.get('C5_POLY_SIGNATURE_TYPE', '0') or '0')
funder = os.environ.get('C5_POLY_FUNDER_ADDRESS', '') or None

try:
    bal_before = clob_balance_usdc(pk, signature_type=sig, funder=funder)
except Exception as e:
    bal_before = f"error: {e}"

print(f"USDC_BEFORE={bal_before}")

# Dry run first
print("\\n--- DRY RUN ---")
dry = process_auto_redeem(dry_run=True)
print(json.dumps(dry, default=str, indent=2))

# Live redeem
print("\\n--- LIVE REDEEM ---")
live = process_auto_redeem(dry_run=False)
print(json.dumps(live, default=str, indent=2))

# Check balance after
try:
    bal_after = clob_balance_usdc(pk, signature_type=sig, funder=funder)
except Exception as e:
    bal_after = f"error: {e}"

print(f"\\nUSDC_AFTER={bal_after}")

# Verify killswitch
from pathlib import Path
ks = Path('/app/logs/killswitch.json')
print(f"KILLSWITCH_ACTIVE={ks.exists()}")
'''

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(VPS, username="root")

    # Write temp script on VPS host
    print("=== Writing redeem script to VPS ===")
    sftp = client.open_sftp()
    with sftp.file('/tmp/_redeem.py', 'w') as f:
        f.write(REDEEM_SCRIPT)
    sftp.close()
    print("  Script uploaded to /tmp/_redeem.py")

    # Copy into container
    print("\n=== Copying script into container ===")
    _, stdout, stderr = client.exec_command(f'docker cp /tmp/_redeem.py {CONTAINER}:/tmp/_redeem.py')
    stdout.read(); stderr.read()
    print("  Copied.")

    # Execute
    print("\n=== Running redeem script inside container ===")
    _, stdout, stderr = client.exec_command(
        f'docker exec {CONTAINER} python3 /tmp/_redeem.py',
        timeout=120
    )
    out = stdout.read().decode()
    err = stderr.read().decode()
    print(out)
    if err:
        # Filter out common warnings
        for line in err.splitlines():
            if 'WARNING' not in line.upper() and 'DeprecationWarning' not in line:
                print(f"  stderr: {line}")

    # Cleanup
    client.exec_command('rm -f /tmp/_redeem.py')
    client.exec_command(f'docker exec {CONTAINER} rm -f /tmp/_redeem.py')
    client.close()
    print("\n✓ Done.")

if __name__ == '__main__':
    run()
