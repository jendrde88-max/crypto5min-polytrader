"""Check luzcifer container status and recent logs."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.248.184.46", username="linuxuser", password="[q4CRaXfa2L2])d*")

cmds = [
    ("Container status", "docker ps --format '{{.Status}}'"),
    ("Last 40 logs", "docker logs crypto5min-polytrader --tail 40 2>&1"),
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
