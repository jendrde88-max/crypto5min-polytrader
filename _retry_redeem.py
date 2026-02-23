#!/usr/bin/env python3
"""
Retry the Sampdoria redeem + check final balance.
Spins up container briefly, redeems, checks balance, stops again.
"""
import paramiko, json, time

VPS = "65.109.240.249"
CONTAINER = "crypto5min-polytrader"

RETRY_SCRIPT = r'''
import sys, os, json, time
sys.path.insert(0, '/app/src')

from crypto5min_polytrader.polymarket_account import clob_balance_usdc
from crypto5min_polytrader.polymarket_redeem import redeem_positions_for_trade

pk = os.environ.get('C5_POLY_PRIVATE_KEY', '')
sig = int(os.environ.get('C5_POLY_SIGNATURE_TYPE', '0') or '0')
funder = os.environ.get('C5_POLY_FUNDER_ADDRESS', '') or None

# Check balance (Dortmund redeem should have confirmed by now)
bal = clob_balance_usdc(pk, signature_type=sig, funder=funder)
print(f'USDC_NOW={bal:.6f}')

# Retry Sampdoria
cid = '0x819b3f58db41c9cc097db7343906fe0c37f2f206b425a2aab1a40be2911c5ae3'
print(f'\n--- Retrying Sampdoria redeem ---')
try:
    result = redeem_positions_for_trade(
        trade={'condition_id': cid},
        dry_run=False,
    )
    print(json.dumps(result, default=str, indent=2))
except Exception as e:
    print(f'ERROR: {e}')

# Wait for on-chain confirmation
time.sleep(10)
bal2 = clob_balance_usdc(pk, signature_type=sig, funder=funder)
print(f'\nFINAL_USDC={bal2:.6f}')
'''

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(VPS, username="root")

    # Start container
    print("=== Starting container briefly ===")
    _, stdout, stderr = client.exec_command(
        'cd /root/crypto5min-polytrader && docker compose up -d',
        timeout=60
    )
    print(stderr.read().decode().strip())
    
    # Wait for container to be ready
    print("Waiting 15s for container startup...")
    time.sleep(15)

    # Upload + run
    sftp = client.open_sftp()
    with sftp.file('/tmp/_retry_redeem.py', 'w') as f:
        f.write(RETRY_SCRIPT)
    sftp.close()

    _, stdout, stderr = client.exec_command(f'docker cp /tmp/_retry_redeem.py {CONTAINER}:/tmp/_retry_redeem.py')
    stdout.read(); stderr.read()

    print("\n=== Running retry redeem ===")
    _, stdout, stderr = client.exec_command(
        f'docker exec {CONTAINER} python3 /tmp/_retry_redeem.py',
        timeout=120
    )
    out = stdout.read().decode()
    err = stderr.read().decode()
    print(out)
    if err:
        for line in err.splitlines():
            if not any(w in line for w in ['WARNING', 'DeprecationWarning', 'UserWarning']):
                print(f"  stderr: {line}")

    # Stop container again
    print("\n=== Stopping container ===")
    _, stdout, stderr = client.exec_command(
        'cd /root/crypto5min-polytrader && docker compose down',
        timeout=60
    )
    print(stderr.read().decode().strip())

    # Verify stopped
    _, stdout, _ = client.exec_command('docker ps --filter name=crypto5min-polytrader --format "{{.Status}}"')
    status = stdout.read().decode().strip()
    if not status:
        print("\n✓ Container stopped. .env intact.")
    else:
        print(f"\n⚠ Still running: {status}")

    client.exec_command('rm -f /tmp/_retry_redeem.py')
    client.close()

if __name__ == '__main__':
    run()
