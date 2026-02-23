"""Upload v0.7.4 release ZIP to VPS auto-update server."""
import paramiko
import os

host = "65.109.240.249"
local_zip = os.path.join(os.path.dirname(__file__), "..", "dist", "Crypto5min_PolyTrader_v0.7.4.zip")
local_zip = os.path.abspath(local_zip)
remote_tmp = "/root/Crypto5min_PolyTrader_v0.7.4.zip"
container = "crypto5min-polytrader"

print(f"Uploading {local_zip} ...")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username="root")

# SCP upload via SFTP
sftp = client.open_sftp()
sftp.put(local_zip, remote_tmp)
sftp.close()
print(f"Uploaded to {host}:{remote_tmp}")

# Docker cp into container /app/releases/
cmd = f"docker cp {remote_tmp} {container}:/app/releases/"
_, stdout, stderr = client.exec_command(cmd)
stdout.read()
err = stderr.read().decode()
if err:
    print(f"docker cp error: {err}")
else:
    print(f"Copied into {container}:/app/releases/")

# Write RELEASE_NOTES.md
notes = "Double-trade fix: snipe no longer duplicates directional trades when delta_first=false. Affects all modes."
cmd2 = f"docker exec {container} bash -c 'echo \"{notes}\" > /app/releases/RELEASE_NOTES.md'"
_, stdout, stderr = client.exec_command(cmd2)
stdout.read()
err2 = stderr.read().decode()
if err2:
    print(f"RELEASE_NOTES error: {err2}")
else:
    print("RELEASE_NOTES.md written")

# Verify
cmd3 = f"docker exec {container} ls -la /app/releases/"
_, stdout, _ = client.exec_command(cmd3)
print("\n/app/releases/ contents:")
print(stdout.read().decode())

# Check /update/latest
import urllib.request
url = "http://65.109.240.249:8602/update/latest?key=drFE4mtZ8lypUsAezwicvVGu7hODfSaQ"
try:
    resp = urllib.request.urlopen(url, timeout=5)
    print(f"\n/update/latest response: {resp.read().decode()}")
except Exception as e:
    print(f"\n/update/latest check failed: {e}")

client.close()
