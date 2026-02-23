from web3 import Web3
import os
w3 = Web3(Web3.HTTPProvider(os.environ.get("C5_POLYGON_RPC", "https://polygon-bor-rpc.publicnode.com")))
try:
    r = w3.eth.get_transaction_receipt("0x31b6cb82e8ce9621b91b36cdc63be4c2a85ba781ad34e0bdbc7e4c9efa06f776")
    print(f"Approve TX status: {r.status} (1=success), block: {r.blockNumber}")
except Exception as e:
    print(f"TX not found/pending: {e}")

addr = "0xf8764f91A3b8f6bF111e9EC5c670B541415D8975"
pol = w3.eth.get_balance(addr) / 1e18
abi = [{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]
usdc = w3.eth.contract(address=Web3.to_checksum_address("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"), abi=abi)
u = usdc.functions.balanceOf(Web3.to_checksum_address(addr)).call() / 1e6
print(f"POL: {pol:.6f}  USDC: {u:.6f}")
