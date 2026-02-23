"""Helper: run commands on luzcifer's VPS via paramiko."""
import paramiko, sys

HOST = "192.248.184.46"
USER = "linuxuser"
PASS = "[q4CRaXfa2L2])d*"

def run(cmd, timeout=30):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(HOST, username=USER, password=PASS, timeout=15)
    stdin, stdout, stderr = c.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode()
    err = stderr.read().decode()
    c.close()
    if out: print(out)
    if err: print("STDERR:", err)
    return out

if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "echo ok"
    run(cmd)
