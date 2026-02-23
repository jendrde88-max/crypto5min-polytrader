import subprocess, os

for f in ['polymarket_redeem.py', 'polymarket_settlement.py', 'polymarket_exec.py']:
    path = f'/app/src/crypto5min_polytrader/{f}'
    if os.path.exists(path):
        r = subprocess.run(['grep', '-n', 'def ', path], capture_output=True, text=True)
        print(f'\n=== {f} ===')
        print(r.stdout)
