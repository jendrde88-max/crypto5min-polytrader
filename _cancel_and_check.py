"""
Cancel stuck pending tx (nonce 454) with a self-send at higher gas,
then do an all-in-one USDC->POL swap using a permit-less approach:
wrap the approval + swap in one sequence once we have enough POL.

Step 1: Cancel stuck approval by sending 0 POL to self at nonce 454 (higher gas).
        This costs very little gas (21000).
Step 2: Then retry the USDC->POL swap.
"""
from web3 import Web3
import os, sys, time

pk = os.environ.get("C5_POLY_PRIVATE_KEY")
if not pk:
    sys.exit("C5_POLY_PRIVATE_KEY not set")

rpc = os.environ.get("C5_POLYGON_RPC", "https://polygon-bor-rpc.publicnode.com")
w3 = Web3(Web3.HTTPProvider(rpc))
acct = w3.eth.account.from_key(pk)
addr = acct.address

confirmed_nonce = w3.eth.get_transaction_count(addr, "latest")
pending_nonce = w3.eth.get_transaction_count(addr, "pending")
gas_price = w3.eth.gas_price
bal = w3.eth.get_balance(addr)

print(f"Wallet: {addr}")
print(f"POL: {bal/1e18:.8f}")
print(f"Nonce confirmed={confirmed_nonce}  pending={pending_nonce}")
print(f"Gas price: {gas_price/1e9:.2f} gwei")

if pending_nonce > confirmed_nonce:
    stuck_nonce = confirmed_nonce
    print(f"\nCancelling stuck tx at nonce {stuck_nonce}...")
    cancel_gas_price = int(gas_price * 2)  # 2x to replace
    cancel_cost = 21000 * cancel_gas_price
    print(f"Cancel cost: {cancel_cost/1e18:.6f} POL")

    if bal < cancel_cost:
        sys.exit(f"Not enough POL even to cancel! Need {cancel_cost/1e18:.6f}, have {bal/1e18:.6f}")

    cancel_tx = {
        "from": addr,
        "to": addr,
        "value": 0,
        "nonce": stuck_nonce,
        "chainId": 137,
        "gasPrice": cancel_gas_price,
        "gas": 21000,
    }
    signed = w3.eth.account.sign_transaction(cancel_tx, private_key=pk)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Cancel TX: {tx_hash.hex()}")
    print("Waiting...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    print(f"Cancel status: {receipt.status} (1=OK)")
    time.sleep(2)
    new_bal = w3.eth.get_balance(addr)
    print(f"POL after cancel: {new_bal/1e18:.8f}")
    new_nonce = w3.eth.get_transaction_count(addr)
    print(f"Nonce now: {new_nonce}")
else:
    print("No stuck tx to cancel.")
    new_bal = bal

# Check if we have enough for approve+swap
approve_cost = 80000 * gas_price
swap_cost = 250000 * gas_price
total = approve_cost + swap_cost
print(f"\nGas needed for approve+swap: {total/1e18:.6f} POL")
print(f"Available: {new_bal/1e18:.6f} POL")

if new_bal < total:
    print(f"NOT ENOUGH POL for swap. Need ~{total/1e18:.4f} POL more.")
    print("Options: send POL from another wallet, or wait for gas price to drop.")
