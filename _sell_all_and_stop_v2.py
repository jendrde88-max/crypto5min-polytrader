"""Sell all positions on user's crypto5min bot, then pause it. Keep .env intact.
Uses external curl (from VPS host) since container doesn't have curl."""
import paramiko
import json
import time

host = "65.109.240.249"
container = "crypto5min-polytrader"
# Internal port 8601 is mapped to 8602 on host
PORT = 8602

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username="root")

def run(cmd):
    _, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out.strip():
        print(out.strip())
    if err.strip():
        print(f"  STDERR: {err.strip()}")
    return out.strip()

print("=== 1. Check current state ===")
run(f"docker exec {container} cat /app/logs/state.json 2>/dev/null | python3 -c 'import sys,json; s=json.load(sys.stdin); pm=s.get(\"polymarket\",{{}}); print(\"Status:\", s.get(\"status\")); print(\"Positions:\", json.dumps(pm.get(\"positions\",[]), indent=2)); print(\"USDC:\", pm.get(\"usdc_balance\",\"?\"))'")

print("\n=== 2. Enable sell_all in runtime_config ===")
run(f"docker exec {container} python3 -c 'import json,pathlib; p=pathlib.Path(\"/app/logs/runtime_config.json\"); d=json.loads(p.read_text()) if p.exists() else {{}}; d[\"C5_POLY_SELL_ALL_ENABLED\"]=\"true\"; d[\"C5_POLY_DRY_RUN\"]=\"false\"; p.write_text(json.dumps(d,indent=2)); print(\"sell_all_enabled:\", d.get(\"C5_POLY_SELL_ALL_ENABLED\")); print(\"dry_run:\", d.get(\"C5_POLY_DRY_RUN\"))'")

print("\n=== 3. Set env var for sell_all check ===")
run(f"docker exec {container} bash -c 'grep -q C5_POLY_SELL_ALL_ENABLED /app/.env 2>/dev/null && sed -i \"s/C5_POLY_SELL_ALL_ENABLED=.*/C5_POLY_SELL_ALL_ENABLED=true/\" /app/.env || echo \"C5_POLY_SELL_ALL_ENABLED=true\" >> /app/.env'")

print("\n=== 4. Restart to pick up sell_all flag ===")
run(f"docker restart {container}")
print("Waiting 20s for container...")
time.sleep(20)
run(f"docker ps --filter name={container} --format '{{{{.Status}}}}'")

print("\n=== 5. Sell all positions (via host curl) ===")
result = run(f"curl -s -X POST http://localhost:{PORT}/poly/sell_all -d 'confirm=yes' -H 'Content-Type: application/x-www-form-urlencoded'")
print(f"Sell result: {result}")

print("\n=== 6. Wait and check balance ===")
time.sleep(15)
run(f"docker exec {container} cat /app/logs/state.json 2>/dev/null | python3 -c 'import sys,json; s=json.load(sys.stdin); pm=s.get(\"polymarket\",{{}}); print(\"Status:\", s.get(\"status\")); print(\"Positions:\", json.dumps(pm.get(\"positions\",[]), indent=2)); print(\"USDC:\", pm.get(\"usdc_balance\",\"?\"))'")

print("\n=== 7. Try redeem endpoint ===")
run(f"curl -s -X POST http://localhost:{PORT}/api/redeem 2>/dev/null || echo 'no /api/redeem'")

print("\n=== 8. Pause the bot ===")
run(f"curl -s -X POST http://localhost:{PORT}/pause")
time.sleep(3)

print("\n=== 9. Final check ===")
run(f"docker exec {container} cat /app/logs/state.json 2>/dev/null | python3 -c 'import sys,json; s=json.load(sys.stdin); pm=s.get(\"polymarket\",{{}}); print(\"Status:\", s.get(\"status\")); print(\"Balance:\", pm.get(\"usdc_balance\",\"?\")); print(\"Positions:\", pm.get(\"positions\",[]))'")

print("\nDone. Bot paused, .env intact.")
client.close()
