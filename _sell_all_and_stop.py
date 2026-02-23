"""Sell all positions on user's crypto5min bot, then pause it. Keep .env intact."""
import paramiko
import json
import time

host = "65.109.240.249"
container = "crypto5min-polytrader"

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

print("=== 1. Check current positions ===")
run(f"docker exec {container} python3 -c \""
    "import json,pathlib;"
    "s=json.loads(pathlib.Path('/app/logs/state.json').read_text());"
    "pm=s.get('polymarket',{{}});"
    "print('Status:', s.get('status'));"
    "print('Positions:', json.dumps(pm.get('positions',[]), indent=2))"
    "\"")

print("\n=== 2. Enable sell_all in runtime_config ===")
run(f"docker exec {container} python3 -c \""
    "import json,pathlib;"
    "p=pathlib.Path('/app/logs/runtime_config.json');"
    "d=json.loads(p.read_text()) if p.exists() else {{}};"
    "d['C5_POLY_SELL_ALL_ENABLED']='true';"
    "d['C5_POLY_DRY_RUN']='false';"
    "p.write_text(json.dumps(d,indent=2));"
    "print('sell_all_enabled:', d.get('C5_POLY_SELL_ALL_ENABLED'));"
    "print('dry_run:', d.get('C5_POLY_DRY_RUN'))"
    "\"")

print("\n=== 3. Also set env var directly for sell_all_enabled check ===")
run(f"docker exec {container} bash -c 'grep -q C5_POLY_SELL_ALL_ENABLED /app/.env 2>/dev/null && sed -i \"s/C5_POLY_SELL_ALL_ENABLED=.*/C5_POLY_SELL_ALL_ENABLED=true/\" /app/.env || echo \"C5_POLY_SELL_ALL_ENABLED=true\" >> /app/.env'")

print("\n=== 4. Restart container to pick up sell_all flag ===")
run(f"docker restart {container}")
print("Waiting 15s for container to start...")
time.sleep(15)
run(f"docker ps --filter name={container} --format '{{{{.Status}}}}'")

print("\n=== 5. Call sell_all endpoint ===")
# Try from inside container first (localhost:8601)
result = run(f"docker exec {container} curl -s -X POST http://localhost:8601/poly/sell_all -d 'confirm=yes' -H 'Content-Type: application/x-www-form-urlencoded'")
print(f"Sell result: {result}")

print("\n=== 6. Wait and check for any remaining positions ===")
time.sleep(10)
run(f"docker exec {container} python3 -c \""
    "import json,pathlib;"
    "s=json.loads(pathlib.Path('/app/logs/state.json').read_text()) if pathlib.Path('/app/logs/state.json').exists() else {{}};"
    "pm=s.get('polymarket',{{}});"
    "print('Positions:', json.dumps(pm.get('positions',[]), indent=2));"
    "print('Balance:', pm.get('usdc_balance','unknown'))"
    "\"")

print("\n=== 7. Check for any redeem-eligible resolved positions ===")
result_redeem = run(f"docker exec {container} curl -s -X POST http://localhost:8601/api/redeem 2>/dev/null || echo 'no redeem endpoint'")
print(f"Redeem result: {result_redeem}")

print("\n=== 8. Pause the bot ===")
run(f"docker exec {container} curl -s -X POST http://localhost:8601/pause")
print("Bot paused.")

print("\n=== 9. Final status check ===")
time.sleep(3)
run(f"docker exec {container} python3 -c \""
    "import json,pathlib;"
    "s=json.loads(pathlib.Path('/app/logs/state.json').read_text()) if pathlib.Path('/app/logs/state.json').exists() else {{}};"
    "print('Status:', s.get('status'));"
    "pm=s.get('polymarket',{{}});"
    "print('Balance:', pm.get('usdc_balance','unknown'));"
    "print('Positions:', pm.get('positions',[]))"
    "\"")

print("\nDone. Bot is paused, .env is intact.")
client.close()
