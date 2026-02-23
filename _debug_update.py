import os
from dotenv import load_dotenv
load_dotenv("/app/config/.env")
print("C5_UPDATE_SERVER =", repr(os.getenv("C5_UPDATE_SERVER")))
print("C5_UPDATE_KEY =", repr(os.getenv("C5_UPDATE_KEY", "NOT SET")[:8]) + "..." if os.getenv("C5_UPDATE_KEY") else "NOT SET")
print("C5_RELEASES_DIR =", repr(os.getenv("C5_RELEASES_DIR")))

# Check if releases dir exists and has files
releases_dir = os.getenv("C5_RELEASES_DIR", "/app/releases")
print(f"\nReleases dir: {releases_dir}")
print(f"Exists: {os.path.isdir(releases_dir)}")
if os.path.isdir(releases_dir):
    import glob
    files = sorted(glob.glob(os.path.join(releases_dir, "*.zip")))
    print(f"ZIPs: {files}")

# Check if _update_server_enabled logic works
val = os.getenv("C5_UPDATE_SERVER", "").strip().lower()
print(f"\nC5_UPDATE_SERVER raw: {repr(val)}")
print(f"Enabled: {val in ('true', '1', 'yes')}")
