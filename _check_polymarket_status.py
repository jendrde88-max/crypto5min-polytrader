#!/usr/bin/env python3
"""Check actual Polymarket status for the 2 positions from the VPS."""
import paramiko, json

VPS = "65.109.240.249"

CHECK_SCRIPT = r'''
import requests, json, sys

WALLET = "0xf8764f91A3b8f6bF111e9EC5c670B541415D8975"
COND_DORTMUND = "0xc98e31d95733702687301fbb701ec462c0a64b46a8dfd5d8550b05785286b4b2"
COND_SAMPDORIA = "0x819b3f58db41c9cc097db7343906fe0c37f2f206b425a2aab1a40be2911c5ae3"

# Check market status for both conditions
print("=" * 60)
print("MARKET STATUS FROM GAMMA API")
print("=" * 60)

for label, cid in [("Dortmund", COND_DORTMUND), ("Sampdoria", COND_SAMPDORIA)]:
    try:
        r = requests.get(f"https://gamma-api.polymarket.com/markets", params={"condition_id": cid}, timeout=15)
        data = r.json()
        markets = data if isinstance(data, list) else [data]
        for m in markets:
            print(f"\n--- {label} ---")
            print(f"  Question:    {m.get('question', '?')}")
            print(f"  Resolved:    {m.get('resolved', '?')}")
            print(f"  Active:      {m.get('active', '?')}")
            print(f"  Closed:      {m.get('closed', '?')}")
            print(f"  Winner:      {m.get('winner', '?')}")
            print(f"  End Date:    {m.get('end_date_iso', '?')}")
            print(f"  Accepting:   {m.get('accepting_orders', '?')}")
            print(f"  Slug:        {m.get('market_slug', '?')}")
    except Exception as e:
        print(f"\n--- {label} ---")
        print(f"  ERROR: {e}")

# Check CLOB market status
print("\n" + "=" * 60)
print("CLOB API MARKET STATUS")
print("=" * 60)

for label, cid in [("Dortmund", COND_DORTMUND), ("Sampdoria", COND_SAMPDORIA)]:
    try:
        r = requests.get(f"https://clob.polymarket.com/markets/{cid}", timeout=15)
        data = r.json()
        if isinstance(data, list):
            for m in data:
                print(f"\n--- {label} (token {m.get('token_id','?')[:16]}...) ---")
                print(f"  Active:      {m.get('active', '?')}")
                print(f"  Closed:      {m.get('closed', '?')}")
                print(f"  Winner:      {m.get('winner', '?')}")
                print(f"  Condition:   {m.get('condition_id', '?')[:20]}...")
        else:
            print(f"\n--- {label} ---")
            print(f"  Response: {json.dumps(data)[:200]}")
    except Exception as e:
        print(f"\n--- {label} ---")
        print(f"  ERROR: {e}")

# Check all positions for this wallet via data API
print("\n" + "=" * 60)
print(f"ALL POSITIONS FOR WALLET {WALLET}")
print("=" * 60)

try:
    r = requests.get(f"https://data-api.polymarket.com/positions", params={"user": WALLET, "sizeThreshold": "0.01"}, timeout=15)
    positions = r.json()
    if not positions:
        print("  NO POSITIONS FOUND (empty)")
    else:
        print(f"  Total positions: {len(positions)}")
        # Group by status
        redeemable = [p for p in positions if p.get('redeemable') or float(p.get('curPrice', 0) or 0) >= 0.999]
        active = [p for p in positions if float(p.get('curPrice', 0) or 0) < 0.999 and not p.get('redeemable')]
        print(f"  Redeemable: {len(redeemable)}")
        print(f"  Active/Tradeable: {len(active)}")
        
        total_value = sum(float(p.get('currentValue', 0) or 0) for p in positions)
        redeem_value = sum(float(p.get('currentValue', 0) or 0) for p in redeemable)
        active_value = sum(float(p.get('currentValue', 0) or 0) for p in active)
        print(f"\n  Total value:      ${total_value:.2f}")
        print(f"  Redeemable value: ${redeem_value:.2f}")
        print(f"  Active value:     ${active_value:.2f}")
        
        if redeemable:
            print(f"\n  REDEEMABLE DETAILS:")
            for p in redeemable[:10]:
                print(f"    {(p.get('market') or p.get('title') or p.get('question') or '?')[:55]}")
                print(f"      Value: ${float(p.get('currentValue',0)):.2f}, Price: {p.get('curPrice')}, Redeemable flag: {p.get('redeemable')}")
                print(f"      Condition: {(p.get('conditionId') or p.get('condition_id') or '?')[:20]}...")
        
        if active:
            print(f"\n  ACTIVE POSITIONS (top 10 by value):")
            active_sorted = sorted(active, key=lambda x: float(x.get('currentValue', 0) or 0), reverse=True)
            for p in active_sorted[:10]:
                print(f"    {(p.get('market') or p.get('title') or p.get('question') or '?')[:55]}")
                print(f"      Value: ${float(p.get('currentValue',0)):.2f}, Size: {p.get('size')}, Price: {p.get('curPrice')}")
except Exception as e:
    print(f"  ERROR: {e}")

# Check USDC balance via CLOB
print("\n" + "=" * 60)
print("CLOB BALANCE")
print("=" * 60)

try:
    import os
    sys.path.insert(0, '/app/src')
    from crypto5min_polytrader.polymarket_account import clob_balance_usdc
    pk = os.environ.get('C5_POLY_PRIVATE_KEY', '')
    sig = int(os.environ.get('C5_POLY_SIGNATURE_TYPE', '0') or '0')
    funder = os.environ.get('C5_POLY_FUNDER_ADDRESS', '') or None
    bal = clob_balance_usdc(pk, signature_type=sig, funder=funder)
    print(f"  USDC Balance: ${bal:.6f}")
except Exception as e:
    print(f"  ERROR: {e}")

# Check the redeem tx status on Polygonscan
print("\n" + "=" * 60)
print("REDEEM TX STATUS")
print("=" * 60)

TX1 = "0xf8bd9583118cbd9fa10f3137d7a4c06ba10c1878f5b680285d40da0b80408c61"
TX2 = "0xd4a6473286169462ac0f8c0b4c6e35725bc56c931ce050f62856bae7d6c3add8"

for label, tx in [("Dortmund", TX1), ("Sampdoria", TX2)]:
    try:
        r = requests.get(f"https://polygon-bor-rpc.publicnode.com", json={
            "jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionReceipt",
            "params": [tx]
        }, timeout=15)
        data = r.json()
        receipt = data.get('result')
        if receipt:
            status = receipt.get('status')
            block = receipt.get('blockNumber')
            gas = receipt.get('gasUsed')
            print(f"\n--- {label} tx: {tx[:20]}... ---")
            print(f"  Status: {'SUCCESS' if status == '0x1' else 'FAILED' if status == '0x0' else status}")
            print(f"  Block:  {int(block, 16) if block else '?'}")
            print(f"  Gas:    {int(gas, 16) if gas else '?'}")
        else:
            print(f"\n--- {label} tx: {tx[:20]}... ---")
            print(f"  NOT FOUND (pending or dropped)")
    except Exception as e:
        print(f"\n--- {label} ---")
        print(f"  ERROR: {e}")
'''

def run():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(VPS, username="root")

    # Need container running briefly for CLOB balance check
    print("Starting container briefly for env vars...")
    _, stdout, stderr = client.exec_command(
        'cd /root/crypto5min-polytrader && docker compose up -d',
        timeout=60
    )
    stderr.read()
    
    import time
    time.sleep(10)

    # Upload script
    sftp = client.open_sftp()
    with sftp.file('/tmp/_check_poly.py', 'w') as f:
        f.write(CHECK_SCRIPT)
    sftp.close()

    _, stdout, stderr = client.exec_command(f'docker cp /tmp/_check_poly.py crypto5min-polytrader:/tmp/_check_poly.py')
    stdout.read(); stderr.read()

    # Run inside container (has requests + py_clob_client + env vars)
    print("Running checks...\n")
    _, stdout, stderr = client.exec_command(
        'docker exec crypto5min-polytrader python3 /tmp/_check_poly.py',
        timeout=120
    )
    out = stdout.read().decode()
    err = stderr.read().decode()
    print(out)
    if err:
        for line in err.splitlines():
            if not any(w in line for w in ['WARNING', 'Deprecation', 'UserWarning']):
                print(f"  stderr: {line}")

    # Stop container again
    print("\nStopping container...")
    _, stdout, stderr = client.exec_command('cd /root/crypto5min-polytrader && docker compose down', timeout=60)
    stderr.read()
    
    _, stdout, _ = client.exec_command('docker ps --filter name=crypto5min-polytrader --format "{{.Status}}"')
    status = stdout.read().decode().strip()
    print("Container stopped." if not status else f"Still running: {status}")

    client.exec_command('rm -f /tmp/_check_poly.py')
    client.close()

if __name__ == '__main__':
    run()
