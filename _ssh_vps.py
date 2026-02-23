#!/usr/bin/env python3
"""SSH helper for our own VPS (65.109.240.249)."""
import paramiko, sys

HOST = "65.109.240.249"
USER = "root"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, timeout=10)

cmd = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'echo connected'
_, out, err = ssh.exec_command(cmd, timeout=60)
o = out.read().decode()
e = err.read().decode()
if o: print(o, end='')
if e: print(e, end='', file=sys.stderr)
ssh.close()
