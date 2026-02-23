"""Check password, paused state, and full .env on luzcifer VPS."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.248.184.46", username="linuxuser", password="[q4CRaXfa2L2])d*")

cmds = [
    ("Full .env (all lines)", "docker exec crypto5min-polytrader cat /app/.env"),
    ("Password from env var", "docker exec crypto5min-polytrader python3 -c \"import os; print('pw:', repr(os.getenv('C5_DASHBOARD_PASSWORD')))\""),
    ("runtime_config exists?", "docker exec crypto5min-polytrader ls -la /app/runtime_config.json 2>&1"),
    ("_paused check", "docker exec crypto5min-polytrader python3 -c \"import os; print('KILLSWITCH:', os.path.exists('/app/logs/killswitch'))\""),
    ("logs dir", "docker exec crypto5min-polytrader ls /app/logs/"),
    ("Docker env vars", "docker inspect crypto5min-polytrader --format '{{range .Config.Env}}{{println .}}{{end}}' | head -20"),
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
