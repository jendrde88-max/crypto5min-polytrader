"""Fix luzcifer's VPS: update config, add CPU limits, deploy v0.7.3, rebuild."""
import paramiko, sys

HOST = "192.248.184.46"
USER = "linuxuser"
PASS = "[q4CRaXfa2L2])d*"

def run(cmd, timeout=60):
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

def upload(local_path, remote_path):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(HOST, username=USER, password=PASS, timeout=15)
    sftp = c.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()
    c.close()
    print(f"Uploaded {local_path} -> {remote_path}")

if __name__ == "__main__":
    BASE = "/home/linuxuser/crypto5min-polytrader"

    # 1) Add update server config to .env
    print("=== Step 1: Add update server config ===")
    run(f"""cat >> {BASE}/config/.env << 'ENVEOF'

# Auto-update server
C5_UPDATE_SERVER_URL=http://65.109.240.249:8602
C5_UPDATE_KEY=drFE4mtZ8lypUsAezwicvVGu7hODfSaQ
ENVEOF""")
    print("Verifying .env update...")
    out = run(f"grep C5_UPDATE {BASE}/config/.env")
    print(f"  -> {out.strip()}")

    # 2) Add CPU limits to docker-compose.yml
    print("\n=== Step 2: Add CPU + memory limits ===")
    run(f"""cat > {BASE}/docker-compose.yml << 'DCEOF'
services:
  crypto5min:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: crypto5min-polytrader
    restart: unless-stopped
    env_file:
      - ./config/.env
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./config:/app/config
      - ./releases:/app/releases
    ports:
      - "${{C5_DASHBOARD_PUBLIC_PORT:-8602}}:8601"
    deploy:
      resources:
        limits:
          cpus: '0.80'
          memory: 1536M
        reservations:
          cpus: '0.25'
          memory: 256M
DCEOF""")
    print("docker-compose.yml updated with CPU limits")

    # 3) Create releases directory and set up for auto-update
    print("\n=== Step 3: Ensure releases dir exists ===")
    run(f"mkdir -p {BASE}/releases")

    # 4) Upload v0.7.3 ZIP
    print("\n=== Step 4: Upload v0.7.3 release ZIP ===")
    local_zip = r"e:\projects\PolyTraderBot\crypto5min-polytrader\dist\Crypto5min_PolyTrader_v0.7.3.zip"
    remote_zip = f"{BASE}/releases/Crypto5min_PolyTrader_v0.7.3.zip"
    try:
        upload(local_zip, remote_zip)
    except Exception as e:
        print(f"Upload failed: {e}")
        print("Trying to copy from existing VPS...")
        run(f"scp -o StrictHostKeyChecking=no root@65.109.240.249:/root/Crypto5min_PolyTrader_v0.7.3.zip {remote_zip} || true")

    # 5) Write RELEASE_NOTES.md
    print("\n=== Step 5: Write RELEASE_NOTES.md ===")
    run(f"""cat > {BASE}/releases/RELEASE_NOTES.md << 'RNEOF'
# v0.7.3 Release Notes

## Dashboard Settings + Docs Refresh

- 4 new dashboard settings: Paper Starting Cash, Ensemble Weight, Quiet Hours, Book Depth Guard
- Full documentation refresh for Paper PnL
- Auto-redeem reliability fixes (relayer v2, rate-limit retry, MATIC check, web3 v7)
- Paper PnL: virtual balance tracking in Dry-Run mode
- 53 dashboard settings verified end-to-end
RNEOF""")

    # 6) Rebuild container
    print("\n=== Step 6: Stop old container ===")
    run(f"cd {BASE} && docker compose down 2>&1 || docker-compose down 2>&1", timeout=30)

    # 7) Clean up old zip and Docker build cache
    print("\n=== Step 7: Clean up ===")
    run("rm -f /home/linuxuser/Crypto5min_PolyTrader_v0.6.9.zip")
    run("docker system prune -f 2>&1")

    # 8) Rebuild and start  
    print("\n=== Step 8: Rebuild and start ===")
    print("Building... (this may take a few minutes on 1-core VPS)")
    out = run(f"cd {BASE} && docker compose up -d --build 2>&1 || docker-compose up -d --build 2>&1", timeout=300)
    print(out)

    # 9) Verify
    print("\n=== Step 9: Verify ===")
    import time
    time.sleep(10)
    out = run("docker ps --format '{{.Names}} {{.Status}}' 2>&1")
    print(f"Container: {out.strip()}")
    out = run(f"docker exec crypto5min-polytrader cat /app/VERSION 2>&1")
    print(f"Version: {out.strip()}")

    print("\n=== DONE ===")
