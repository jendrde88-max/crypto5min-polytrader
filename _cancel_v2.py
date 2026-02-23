"""Cancel stuck nonce 454 using polygon-rpc.com and EIP-1559 tx."""
from web3 import Web3
import os, sys, time

pk = os.environ.get("C5_POLY_PRIVATE_KEY")
if not pk:
    sys.exit("C5_POLY_PRIVATE_KEY not set")

# Try multiple RPCs
RPCS = [
    "https://polygon-rpc.com",
    "https://polygon-bor-rpc.publicnode.com",
    "https://1rpc.io/matic",
]

for rpc in RPCS:
    try:
        w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 10}))
        if w3.is_connected():
            print(f"Connected to {rpc}")
            break
    except:
        continue
else:
    sys.exit("Cannot connect to any RPC")

acct = w3.eth.account.from_key(pk)
addr = acct.address

bal = w3.eth.get_balance(addr)
nonce_conf = w3.eth.get_transaction_count(addr, "latest")
nonce_pend = w3.eth.get_transaction_count(addr, "pending")
block = w3.eth.get_block("latest")
base_fee = block.get("baseFeePerGas", 30 * 10**9)

print(f"Wallet: {addr}")
print(f"POL: {bal/1e18:.8f}")
print(f"Nonce: confirmed={nonce_conf} pending={nonce_pend}")
print(f"Base fee: {base_fee/1e9:.2f} gwei")

# Use nonce of confirmed (to replace any pending)
cancel_nonce = nonce_conf
# Set very high priority fee to ensure inclusion
max_priority = int(50 * 1e9)  # 50 gwei priority
max_fee = int(base_fee * 3 + max_priority)  # 3x base + priority

cancel_cost_max = 21000 * max_fee
print(f"Max cancel cost: {cancel_cost_max/1e18:.6f} POL")

if bal < cancel_cost_max:
    # Fall back to legacy tx with lower gas
    print("Using legacy tx with moderate gas...")
    gas_price = int(base_fee * 1.5)
    cancel_tx = {
        "from": addr, "to": addr, "value": 0,
        "nonce": cancel_nonce, "chainId": 137,
        "gasPrice": gas_price, "gas": 21000,
    }
    cost = 21000 * gas_price
    print(f"Legacy cancel cost: {cost/1e18:.6f} POL")
else:
    cancel_tx = {
        "from": addr, "to": addr, "value": 0,
        "nonce": cancel_nonce, "chainId": 137,
        "maxFeePerGas": max_fee,
        "maxPriorityFeePerGas": max_priority,
        "gas": 21000,
        "type": 2,
    }

signed = w3.eth.account.sign_transaction(cancel_tx, private_key=pk)
print(f"Broadcasting cancel for nonce {cancel_nonce}...")

# Try broadcasting on all RPCs
for rpc in RPCS:
    try:
        w_alt = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 10}))
        tx_hash = w_alt.eth.send_raw_transaction(signed.raw_transaction)
        print(f"  Sent via {rpc}: {tx_hash.hex()}")
    except Exception as e:
        print(f"  {rpc}: {e}")

print("Waiting for confirmation (up to 5 min)...")
try:
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    print(f"Confirmed! status={receipt.status} block={receipt.blockNumber}")
    new_bal = w3.eth.get_balance(addr)
    new_nonce = w3.eth.get_transaction_count(addr)
    print(f"New POL: {new_bal/1e18:.8f}  Nonce: {new_nonce}")
except Exception as e:
    print(f"Timeout: {e}")
    # Check if maybe it went through anyway
    new_nonce = w3.eth.get_transaction_count(addr)
    print(f"Current nonce: {new_nonce}")
