import subprocess
r = subprocess.run(['sed', '-n', '66,300p', '/app/src/crypto5min_polytrader/polymarket_settlement.py'], capture_output=True, text=True)
print(r.stdout[:4000])
