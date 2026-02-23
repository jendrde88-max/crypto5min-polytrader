"""Start the bot for luzcifer - unpause and apply your recommended settings."""
import paramiko
import json

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('192.248.184.46', username='linuxuser', password='[q4CRaXfa2L2])d*', timeout=15)

base = '/home/linuxuser/crypto5min-polytrader'

# 1) Clear killswitch
cmd = f'docker exec crypto5min-polytrader bash -c \'echo "{{}}" > /app/logs/killswitch.json\''
stdin, stdout, stderr = c.exec_command(cmd, timeout=10)
stdout.read()
print('Killswitch cleared')

# 2) Update state to "resuming"
import time
state = json.dumps({"status": "resuming", "ts": time.time()})
cmd = f"docker exec crypto5min-polytrader bash -c 'echo {json.dumps(state)} > /app/logs/state.json'"
stdin, stdout, stderr = c.exec_command(cmd, timeout=10)
stdout.read()
print('State set to resuming')

# 3) Apply your recommended settings via runtime_config
rc = {
    "C5_MODE": "paper",
    "C5_POLY_DRY_RUN": "true",
    "C5_SYMBOL": "BTC-USD",
    "C5_SYMBOLS": "BTC-USD",
    "C5_DELTA_FIRST": "false",
    "C5_DELTA_PRICING": "true",
    "C5_SNIPE_ENABLED": "true",
    "C5_CONFIDENCE_THRESHOLD": "0.52",
    "C5_POLY_KELLY_FRACTION": "0.5",
    "C5_POLY_HIGH_RISK": "true",
    "C5_POLY_BET_PERCENT": "50",
}
rc_json = json.dumps(rc, indent=2)
sftp = c.open_sftp()
with sftp.open(f'{base}/logs/runtime_config.json', 'w') as f:
    f.write(rc_json)
sftp.close()
print('Runtime config written with recommended settings')

# 4) Verify
stdin, stdout, stderr = c.exec_command(f'docker exec crypto5min-polytrader cat /app/logs/state.json', timeout=10)
print('State:', stdout.read().decode().strip())
stdin, stdout, stderr = c.exec_command(f'docker exec crypto5min-polytrader cat /app/logs/runtime_config.json', timeout=10)
print('Runtime config:', stdout.read().decode().strip())
stdin, stdout, stderr = c.exec_command(f'docker exec crypto5min-polytrader cat /app/logs/killswitch.json', timeout=10)
print('Killswitch:', stdout.read().decode().strip())

c.close()
print('\nBot should start on next loop iteration!')
