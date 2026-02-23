"""Fix luzcifer's setup: write private key + funder to .env inside container, then restart."""
import paramiko

host = "192.248.184.46"
user = "linuxuser"
passwd = "[q4CRaXfa2L2])d*"

PK = "0x596be413f587aa9c6070411e67a716d8610a4c198ea80ef999b7320addb21008"
FUNDER = "0x95A02018fd6f9C48811A53d039Aa9e32BeB295d9"
CONTAINER = "crypto5min-polytrader"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=user, password=passwd)

def run(cmd):
    _, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out.strip():
        print(out.strip())
    if err.strip():
        print(f"  STDERR: {err.strip()}")
    return out.strip()

print("=== 1. Check current .env for key/funder lines ===")
run(f"docker exec {CONTAINER} grep -n 'C5_POLY_PRIVATE_KEY\\|C5_POLY_FUNDER' /app/.env")

print("\n=== 2. Set private key in .env ===")
# Remove any existing lines, then append fresh
run(f"docker exec {CONTAINER} sed -i '/^C5_POLY_PRIVATE_KEY/d' /app/.env")
run(f"docker exec {CONTAINER} bash -c 'echo \"C5_POLY_PRIVATE_KEY={PK}\" >> /app/.env'")

print("\n=== 3. Set funder address in .env ===")
run(f"docker exec {CONTAINER} sed -i '/^C5_POLY_FUNDER/d' /app/.env")
run(f"docker exec {CONTAINER} bash -c 'echo \"C5_POLY_FUNDER_ADDRESS={FUNDER}\" >> /app/.env'")

print("\n=== 4. Verify .env has the values ===")
run(f"docker exec {CONTAINER} grep -n 'C5_POLY_PRIVATE_KEY\\|C5_POLY_FUNDER' /app/.env")

print("\n=== 5. Restart container ===")
run(f"docker restart {CONTAINER}")

print("\n=== 6. Wait for container to come up ===")
import time
time.sleep(10)
run(f"docker ps --filter name={CONTAINER} --format 'table {{{{.Status}}}}\\t{{{{.Ports}}}}'")

print("\n=== 7. Check state ===")
time.sleep(5)
run(f"docker exec {CONTAINER} cat /app/logs/state.json 2>/dev/null | head -5")

print("\nDone. Dashboard should be at http://192.248.184.46:8602/")
client.close()
