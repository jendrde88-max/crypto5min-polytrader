#!/usr/bin/env python3
"""Debug reconcile logic directly."""
import json, time, os

os.chdir("/app")

trades = json.load(open("logs/poly_trades.json"))
now = int(time.time())
print(f"now={now}")

# Check env var
drop_env = os.environ.get("C5_POLY_REDEEM_DROP_SECONDS", "NOT_SET")
print(f"C5_POLY_REDEEM_DROP_SECONDS env = {drop_env!r}")

# Parse same way as the code
def _getenv(name, default=''):
    return (os.getenv(name) or default).strip()

def _getint(name, default):
    v = _getenv(name)
    if not v:
        return default
    try:
        return int(float(v))
    except:
        return default

drop_threshold = _getint("C5_POLY_REDEEM_DROP_SECONDS", 600)
print(f"drop_threshold = {drop_threshold}")

# Try getting a receipt for one of the tx hashes
from web3 import Web3
rpc = (_getenv("C5_POLYGON_RPC", "") or "https://polygon-bor-rpc.publicnode.com").strip()
print(f"RPC: {rpc}")
w3 = Web3(Web3.HTTPProvider(rpc))
print(f"Connected: {w3.is_connected()}")

for t in trades:
    if t.get("redeem_status") == "submitted":
        txh = str(t.get("redeem_tx_hash") or "").strip()
        if not txh:
            continue
        if not txh.startswith("0x"):
            txh = "0x" + txh
        txh = txh.lower()
        
        try:
            receipt = w3.eth.get_transaction_receipt(txh)
            receipt_val = "GOT_RECEIPT"
            print(f"TX {txh[:20]}... => RECEIPT FOUND: status={receipt.get('status') if isinstance(receipt, dict) else getattr(receipt, 'status', 'UNKNOWN')}")
        except Exception as e:
            receipt = None
            receipt_val = f"EXCEPTION: {type(e).__name__}: {str(e)[:80]}"
            print(f"TX {txh[:20]}... => {receipt_val}")
        
        if not receipt:
            submitted_ts = t.get("redeem_submitted_ts", 0)
            age = now - int(float(submitted_ts or 0))
            should_drop = bool(submitted_ts) and age > drop_threshold
            print(f"  submitted_ts={submitted_ts} age={age} threshold={drop_threshold} should_drop={should_drop}")
        
        break  # Just check one to avoid RPC rate limits
