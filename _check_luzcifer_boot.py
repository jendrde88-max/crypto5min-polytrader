"""Check luzcifer app.log from start — how long has the bot been running?"""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.248.184.46", username="linuxuser", password="[q4CRaXfa2L2])d*")

cmds = [
    ("First 10 lines app.log", "docker exec crypto5min-polytrader head -10 /app/logs/app.log"),
    ("Any training lines", "docker exec crypto5min-polytrader grep -i 'train\\|retrain\\|model.*fit\\|FITTING' /app/logs/app.log | tail -20"),
    ("Status lines", "docker exec crypto5min-polytrader grep -iE 'status|state.*ok|startup|signal' /app/logs/app.log | tail -20"),
    ("Warnings", "docker exec crypto5min-polytrader grep -i 'warning\\|warn' /app/logs/app.log | tail -20"),
    ("Container start time", "docker inspect crypto5min-polytrader --format '{{.State.StartedAt}}'"),
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
