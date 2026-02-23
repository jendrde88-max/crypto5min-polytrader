import subprocess
r = subprocess.run(['sed', '-n', '472,522p', '/app/src/crypto5min_polytrader/polymarket_redeem.py'], capture_output=True, text=True)
print(r.stdout)
