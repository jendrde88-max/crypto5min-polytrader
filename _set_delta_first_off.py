"""SSH to VPS and set delta_first=false in runtime_config.json"""
import paramiko, json

host = "65.109.240.249"
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username="root")

# Read current config
cmd_read = "docker exec crypto5min-polytrader cat /app/logs/runtime_config.json"
_, stdout, _ = client.exec_command(cmd_read)
config = json.loads(stdout.read().decode())

# Set delta_first=false
config["C5_DELTA_FIRST"] = "false"
new_json = json.dumps(config, indent=2)

# Write back
cmd_write = f"docker exec crypto5min-polytrader bash -c 'cat > /app/logs/runtime_config.json << EOFCFG\n{new_json}\nEOFCFG'"
_, stdout, stderr = client.exec_command(cmd_write)
stdout.read()
err = stderr.read().decode()
if err:
    print(f"ERROR: {err}")

# Verify
_, stdout, _ = client.exec_command(cmd_read)
verify = json.loads(stdout.read().decode())
print(f"C5_DELTA_FIRST = {verify.get('C5_DELTA_FIRST')}")
print("OK - delta_first is now OFF. ML directional trades re-enabled.")

client.close()
