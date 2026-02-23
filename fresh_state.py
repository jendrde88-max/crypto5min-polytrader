import sys, os, json, time
sys.path.insert(0, '/app/src')

with open('/app/config/.env') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, _, v = line.partition('=')
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from datetime import datetime, timezone

# 1. Fresh snapshot
snap = json.load(open('/app/logs/poly_snapshot.json'))
snap_age = time.time() - snap.get('ts', 0)
print("=== CURRENT SNAPSHOT ===")
print(f"  Age: {snap_age/60:.1f} min ago")
print(f"  Active positions: {snap.get('active_positions')}")
print(f"  Positions value: ${snap.get('positions_value_usdc', 0):.2f}")
print(f"  CLOB balance: ${snap.get('clob_balance_usdc', 0):.2f}")
print(f"  Total equity: ${snap.get('total_equity_usdc', 0):.2f}")

# 2. Wallet address from env
wallet = os.environ.get('C5_POLY_WALLET_ADDRESS', '')
print(f"\n  Wallet: {wallet[:20]}..." if wallet else "\n  Wallet: NOT SET")

# 3. Trades with resolved_outcome set
trades = json.load(open('/app/logs/poly_trades.json'))
resolved_wins = [t for t in trades if t.get('resolved_outcome') and t.get('resolved_outcome').upper() in ('YES','WIN','1','TRUE','UP')]
resolved_losses = [t for t in trades if t.get('resolved_outcome') and t.get('resolved_outcome').upper() in ('NO','LOSS','0','FALSE','DOWN')]
unresolved_filled = [t for t in trades if t.get('order_status') == 'filled' and not t.get('resolved_outcome') and not t.get('redeem_tx_hash')]
print(f"\n=== TRADE OUTCOMES ===")
print(f"  Resolved WINS: {len(resolved_wins)}")
print(f"  Resolved LOSSES: {len(resolved_losses)}")
print(f"  Filled + unresolved: {len(unresolved_filled)}")
print(f"  Already redeemed (has tx_hash): {len([t for t in trades if t.get('redeem_tx_hash')])}")

# Show unique resolved_outcome values
outcomes = set(t.get('resolved_outcome') for t in trades if t.get('resolved_outcome'))
print(f"\n  Unique resolved_outcome values: {outcomes}")

# 4. Try Polymarket data API with correct wallet
import requests
if wallet:
    url = f"https://data-api.polymarket.com/positions?user={wallet}&sizeThreshold=0.01&limit=50"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        positions = data if isinstance(data, list) else data.get('data', data.get('positions', []))
        print(f"\n=== POLYMARKET API (live) ===")
        print(f"  Positions returned: {len(positions)}")
        total_val = 0
        for p in positions[:10]:
            slug = (p.get('market') or p.get('conditionId',''))[:35]
            size = float(p.get('size', p.get('shares', 0)) or 0)
            val = float(p.get('value', p.get('currentValue', 0)) or 0)
            price = float(p.get('curPrice', p.get('price', 0)) or 0)
            total_val += val
            print(f"  {slug} | {size:.2f}sh @ {price:.3f} = ${val:.2f}")
        if positions:
            print(f"  Total: ${total_val:.2f}")
    except Exception as e:
        print(f"\n  API error: {e}")
