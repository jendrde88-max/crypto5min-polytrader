import subprocess
r = subprocess.run(['cat', '/app/src/crypto5min_polytrader/polymarket_account.py'], capture_output=True, text=True)
print(r.stdout[:6000])
