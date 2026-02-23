"""Add update server config to luzcifer's .env"""
import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('192.248.184.46', username='linuxuser', password='[q4CRaXfa2L2])d*', timeout=15)

env_path = '/home/linuxuser/crypto5min-polytrader/config/.env'

# Append update server lines
lines = [
    '',
    '# Auto-update server',
    'C5_UPDATE_SERVER_URL=http://65.109.240.249:8602',
    'C5_UPDATE_KEY=drFE4mtZ8lypUsAezwicvVGu7hODfSaQ',
]
for line in lines:
    cmd = f'echo "{line}" >> {env_path}'
    stdin, stdout, stderr = c.exec_command(cmd)
    stdout.read()

# Verify
stdin, stdout, stderr = c.exec_command(f'grep C5_UPDATE {env_path}')
print('Update config added:')
print(stdout.read().decode())

c.close()
