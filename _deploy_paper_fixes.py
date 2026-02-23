#!/usr/bin/env python3
"""Deploy paper-mode fixes to luzcifer VPS.

Deploys:
  1. templates/partials/live.html  → hide gas line in paper mode (ACCOUNT card)
  2. src/crypto5min_polytrader/paper_pnl.py → add total_equity_usdc to snapshot
Then restarts the container.
"""
import paramiko, os, time

HOST = '192.248.184.46'
USER = 'linuxuser'
PASS = r'[q4CRaXfa2L2])d*'
CONTAINER = 'crypto5min-polytrader'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = [
    (os.path.join(ROOT, 'templates', 'partials', 'live.html'),
     '/tmp/live.html',
     '/app/templates/partials/live.html'),
    (os.path.join(ROOT, 'src', 'crypto5min_polytrader', 'paper_pnl.py'),
     '/tmp/paper_pnl.py',
     '/app/src/crypto5min_polytrader/paper_pnl.py'),
]

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS)
    sftp = ssh.open_sftp()

    for local, remote_tmp, container_path in FILES:
        print(f'  SFTP {os.path.basename(local)} → {remote_tmp}')
        sftp.put(local, remote_tmp)
        cmd = f'docker cp {remote_tmp} {CONTAINER}:{container_path}'
        print(f'  docker cp → {container_path}')
        _in, _out, _err = ssh.exec_command(cmd)
        rc = _out.channel.recv_exit_status()
        if rc != 0:
            print(f'  ERROR: {_err.read().decode().strip()}')
            return
        print(f'  ✓ copied')

    sftp.close()

    print(f'\n  Restarting {CONTAINER}...')
    _in, _out, _err = ssh.exec_command(f'docker restart {CONTAINER}')
    rc = _out.channel.recv_exit_status()
    print(f'  restart rc={rc}')
    if rc != 0:
        print(f'  ERROR: {_err.read().decode().strip()}')
        ssh.close()
        return

    print('  Waiting 15s for container to boot...')
    time.sleep(15)

    # Quick health check
    _in, _out, _err = ssh.exec_command(f'docker exec {CONTAINER} cat /app/VERSION')
    ver = _out.read().decode().strip()
    print(f'  VERSION inside container: {ver}')

    # Verify the fix is present
    _in, _out, _err = ssh.exec_command(
        f"docker exec {CONTAINER} grep -c \"cfg.mode != 'paper'\" /app/templates/partials/live.html"
    )
    count = _out.read().decode().strip()
    print(f'  live.html paper guard count: {count} (expect 1)')

    _in, _out, _err = ssh.exec_command(
        f"docker exec {CONTAINER} grep -c 'total_equity_usdc' /app/src/crypto5min_polytrader/paper_pnl.py"
    )
    count2 = _out.read().decode().strip()
    print(f'  paper_pnl.py total_equity_usdc count: {count2} (expect 1)')

    ssh.close()
    print('\n  ✅ DONE — fixes deployed to luzcifer VPS')

if __name__ == '__main__':
    main()
