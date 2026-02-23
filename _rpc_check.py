"""Check nonce state and try RPC health."""
from web3 import Web3
import os

rpc = os.environ.get("C5_POLYGON_RPC", "https://polygon-bor-rpc.publicnode.com")
print(f"RPC: {rpc}")

w3 = Web3(Web3.HTTPProvider(rpc))
addr = "0xf8764f91A3b8f6bF111e9EC5c670B541415D8975"

nonce = w3.eth.get_transaction_count(addr)
pending_nonce = w3.eth.get_transaction_count(addr, "pending")
bal = w3.eth.get_balance(addr)
gas_price = w3.eth.gas_price

print(f"Nonce (confirmed): {nonce}")
print(f"Nonce (pending):   {pending_nonce}")
print(f"POL balance:       {bal / 1e18:.8f}")
print(f"Gas price:         {gas_price / 1e9:.2f} gwei")
print(f"Approve cost est:  {80000 * gas_price / 1e18:.6f} POL")
print(f"Swap cost est:     {250000 * gas_price / 1e18:.6f} POL")
print(f"Total gas est:     {330000 * gas_price / 1e18:.6f} POL")
print(f"Affordable:        {bal > 330000 * gas_price}")

# Try alternative RPCs
alt_rpcs = [
    "https://polygon-rpc.com",
    "https://rpc-mainnet.maticvigil.com",
    "https://polygon.llamarpc.com",
]
for r in alt_rpcs:
    try:
        w = Web3(Web3.HTTPProvider(r, request_kwargs={"timeout": 5}))
        bn = w.eth.block_number
        gp = w.eth.gas_price / 1e9
        print(f"  ALT {r}: block={bn} gas={gp:.1f}gwei OK")
    except Exception as e:
        print(f"  ALT {r}: FAIL ({e})")
