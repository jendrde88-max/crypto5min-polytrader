"""Check all wallet token balances on Polygon."""
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://polygon-bor-rpc.publicnode.com"))
addr = "0xf8764f91A3b8f6bF111e9EC5c670B541415D8975"

# Native POL
pol = w3.eth.get_balance(addr)
print(f"POL (native gas): {pol / 1e18:.6f}")

abi = [
    {
        "constant": True,
        "inputs": [{"name": "a", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    }
]

tokens = {
    "USDC.e": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    "USDC (native)": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
    "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
    "WMATIC/WPOL": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
}

for name, address in tokens.items():
    c = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
    bal = c.functions.balanceOf(Web3.to_checksum_address(addr)).call()
    decimals = 18 if "ETH" in name or "MATIC" in name or "POL" in name else 6
    print(f"{name}: {bal / 10**decimals:.6f}")
