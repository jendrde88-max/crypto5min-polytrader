"""Cancel stuck nonce 454 using polygon-rpc.com with POA middleware."""
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
import os, sys, time

pk = os.environ.get("C5_POLY_PRIVATE_KEY")
if not pk:
    sys.exit("C5_POLY_PRIVATE_KEY not set")

# Try main configured RPC first, then alternatives
main_rpc = os.environ.get("C5_POLYGON_RPC", "https://polygon-bor-rpc.publicnode.com")
RPCS = [main_rpc, "https://polygon-rpc.com", "https://1rpc.io/matic"]

def make_w3(rpc):
    w = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 15}))
    w.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    return w

w3 = None
for rpc in RPCS:
    try:
        w3 = make_w3(rpc)
        _ = w3.eth.block_number
        print(f"Connected: {rpc}")
        break
    except Exception as e:
        print(f"Skip {rpc}: {e}")
if not w3:
    sys.exit("No RPC available")

acct = w3.eth.account.from_key(pk)
addr = acct.address
bal = w3.eth.get_balance(addr)
nonce_conf = w3.eth.get_transaction_count(addr, "latest")
nonce_pend = w3.eth.get_transaction_count(addr, "pending")
gas_price = w3.eth.gas_price

print(f"Wallet: {addr}")
print(f"POL: {bal/1e18:.8f}")
print(f"Nonce: confirmed={nonce_conf} pending={nonce_pend}")
print(f"Gas price: {gas_price/1e9:.2f} gwei")

if nonce_pend <= nonce_conf:
    print("No stuck tx. Nonce is clean.")
    sys.exit(0)

# Cancel at confirmed nonce with 2x gas
cancel_nonce = nonce_conf
cancel_gas = int(gas_price * 2)
cost = 21000 * cancel_gas
print(f"\nCancel nonce {cancel_nonce} with {cancel_gas/1e9:.1f} gwei (cost: {cost/1e18:.6f} POL)")

if bal < cost:
    # Try with 1.1x instead
    cancel_gas = int(gas_price * 1.1)
    cost = 21000 * cancel_gas
    print(f"Reduced to {cancel_gas/1e9:.1f} gwei (cost: {cost/1e18:.6f} POL)")
    if bal < cost:
        sys.exit(f"Not enough POL: have {bal/1e18:.6f}, need {cost/1e18:.6f}")

cancel_tx = {
    "from": addr, "to": addr, "value": 0,
    "nonce": cancel_nonce, "chainId": 137,
    "gasPrice": cancel_gas, "gas": 21000,
}
signed = w3.eth.account.sign_transaction(cancel_tx, private_key=pk)

# Broadcast on all RPCs
for r in RPCS:
    try:
        w_alt = make_w3(r)
        h = w_alt.eth.send_raw_transaction(signed.raw_transaction)
        print(f"Sent via {r}: {h.hex()}")
    except Exception as e:
        err = str(e)[:80]
        print(f"  {r}: {err}")

print("Waiting (up to 5 min)...")
try:
    receipt = w3.eth.wait_for_transaction_receipt(signed.hash, timeout=300)
    print(f"Confirmed! status={receipt.status}")
except:
    pass

new_nonce = w3.eth.get_transaction_count(addr, "latest")
new_pend = w3.eth.get_transaction_count(addr, "pending")
new_bal = w3.eth.get_balance(addr)
print(f"\nAfter: nonce={new_nonce} pending={new_pend} POL={new_bal/1e18:.8f}")

# Check if we can now do the swap
approve_gas_cost = 80000 * gas_price
swap_gas_cost = 250000 * gas_price
total_needed = approve_gas_cost + swap_gas_cost
print(f"Gas for approve+swap: {total_needed/1e18:.6f} POL")
if new_bal >= total_needed:
    print("ENOUGH POL for USDC->POL swap!")
else:
    deficit = (total_needed - new_bal) / 1e18
    print(f"Still need {deficit:.4f} more POL for swap gas")
