"""Deeper diagnostics for luzcifer — check runner, training, errors."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.248.184.46", username="linuxuser", password="[q4CRaXfa2L2])d*")

cmds = [
    ("Full logs (first 80 lines)", "docker logs crypto5min-polytrader 2>&1 | head -80"),
    ("Any errors/warnings", "docker logs crypto5min-polytrader 2>&1 | grep -iE 'error|exception|traceback|fail|warn|train|model|runner|paper' | tail -40"),
    ("Config mode check", "docker exec crypto5min-polytrader python3 -c \"import json; c=json.load(open('/app/runtime_config.json')) if __import__('os').path.exists('/app/runtime_config.json') else {}; print('mode:', c.get('C5_MODE','not set')); print('enabled:', c.get('C5_ENABLED','not set'))\""),
    (".env mode", "docker exec crypto5min-polytrader grep -E 'C5_MODE|C5_ENABLED' /app/.env 2>/dev/null || echo 'no .env or no match'"),
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
