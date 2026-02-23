"""Check runtime_config in logs dir and state.json."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.248.184.46", username="linuxuser", password="[q4CRaXfa2L2])d*")

cmds = [
    ("runtime_config in logs", "docker exec crypto5min-polytrader cat /app/logs/runtime_config.json 2>&1"),
    ("state.json", "docker exec crypto5min-polytrader cat /app/logs/state.json 2>&1"),
    ("poly_snapshot.json (last 5 lines)", "docker exec crypto5min-polytrader tail -5 /app/logs/poly_snapshot.json 2>&1"),
    ("app.log last 40 lines", "docker exec crypto5min-polytrader tail -40 /app/logs/app.log 2>&1"),
]

for label, cmd in cmds:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    _, o, e = ssh.exec_command(cmd)
    out = o.read().decode()
    err = e.read().decode()
    print(out or err or "(empty)")

ssh.close()
