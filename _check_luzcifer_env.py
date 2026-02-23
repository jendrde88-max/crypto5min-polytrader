"""Check luzcifer's .env and runtime_config for why runner isn't starting."""
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.248.184.46", username="linuxuser", password="[q4CRaXfa2L2])d*")

cmds = [
    ("Full .env (redacted keys)", "docker exec crypto5min-polytrader sh -c 'cat /app/.env | grep -vE \"KEY|SECRET|PASS|TOKEN|PRIV\" || echo \"no .env\"'"),
    (".env MODE and ENABLED lines", "docker exec crypto5min-polytrader sh -c 'cat /app/.env | grep -iE \"MODE|ENABLE|SYMBOL\" || echo \"none found\"'"),
    ("runtime_config.json", "docker exec crypto5min-polytrader sh -c 'cat /app/runtime_config.json 2>/dev/null || echo \"no runtime_config.json\"'"),
    ("All .env lines (count)", "docker exec crypto5min-polytrader sh -c 'wc -l /app/.env 2>/dev/null || echo \"no .env\"'"),
    ("Runner code check", "docker exec crypto5min-polytrader sh -c 'grep -n \"C5_ENABLED\\|C5_MODE\\|runner\" /app/src/crypto5min_polytrader/web.py | head -20'"),
    ("Process list", "docker exec crypto5min-polytrader ps aux 2>/dev/null || docker exec crypto5min-polytrader sh -c 'ls /proc/*/cmdline 2>/dev/null | head -5'"),
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
