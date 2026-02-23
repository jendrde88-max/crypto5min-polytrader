#!/usr/bin/env python3
"""Swap a small amount of USDC.e -> POL via QuickSwap to refill gas."""
from __future__ import annotations
import os, sys, time
from web3 import Web3

POLYGON_CHAIN_ID = 137
USDC_E = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
WMATIC = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
ROUTER = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
SLIPPAGE_BPS = 200

_ERC20_ABI = [
    {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
    {"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"type":"function"},
    {"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"type":"function"},
]

_ROUTER_ABI = [
    {"name":"getAmountsOut","type":"function","stateMutability":"view",
     "inputs":[{"name":"amountIn","type":"uint256"},{"name":"path","type":"address[]"}],
     "outputs":[{"name":"amounts","type":"uint256[]"}]},
    {"name":"swapExactTokensForETH","type":"function","stateMutability":"nonpayable",
     "inputs":[{"name":"amountIn","type":"uint256"},{"name":"amountOutMin","type":"uint256"},
               {"name":"path","type":"address[]"},{"name":"to","type":"address"},
               {"name":"deadline","type":"uint256"}],
     "outputs":[{"name":"amounts","type":"uint256[]"}]},
]

SWAP_USDC = 2.0  # swap $2 USDC -> POL

def main():
    pk = os.environ.get("C5_POLY_PRIVATE_KEY")
    if not pk:
        sys.exit("ERROR: C5_POLY_PRIVATE_KEY not set")
    rpc = os.environ.get("C5_POLYGON_RPC", "https://polygon-bor-rpc.publicnode.com")

    w3 = Web3(Web3.HTTPProvider(rpc))
    acct = w3.eth.account.from_key(pk)
    addr = acct.address

    usdc_addr = Web3.to_checksum_address(USDC_E)
    wmatic_addr = Web3.to_checksum_address(WMATIC)
    router_addr = Web3.to_checksum_address(ROUTER)

    usdc = w3.eth.contract(address=usdc_addr, abi=_ERC20_ABI)
    router = w3.eth.contract(address=router_addr, abi=_ROUTER_ABI)

    pol_bal = w3.eth.get_balance(addr) / 1e18
    usdc_bal = usdc.functions.balanceOf(addr).call() / 1e6
    print(f"Wallet: {addr}")
    print(f"POL:  {pol_bal:.6f}")
    print(f"USDC: {usdc_bal:.6f}")

    sell_raw = int(SWAP_USDC * 1e6)
    if usdc_bal < SWAP_USDC:
        sys.exit(f"ERROR: not enough USDC (have {usdc_bal:.2f}, need {SWAP_USDC})")

    path = [usdc_addr, wmatic_addr]
    amounts = router.functions.getAmountsOut(sell_raw, path).call()
    expected_pol = amounts[1] / 1e18
    min_out = int(amounts[1] * (10000 - SLIPPAGE_BPS) / 10000)
    print(f"\nSwapping {SWAP_USDC} USDC -> ~{expected_pol:.4f} POL")

    # check/set allowance
    gas_price = int(w3.eth.gas_price * 1.5)  # 50% bump for reliability
    allowance = usdc.functions.allowance(addr, router_addr).call()
    if allowance < sell_raw:
        print("Approving USDC spend on QuickSwap router...")
        approve_tx = usdc.functions.approve(
            router_addr, 2**256 - 1
        ).build_transaction({
            "from": addr, "nonce": w3.eth.get_transaction_count(addr),
            "chainId": POLYGON_CHAIN_ID, "gasPrice": gas_price, "gas": 80000,
        })
        signed_a = w3.eth.account.sign_transaction(approve_tx, private_key=pk)
        ah = w3.eth.send_raw_transaction(signed_a.raw_transaction)
        print(f"Approve TX: {ah.hex()}")
        w3.eth.wait_for_transaction_receipt(ah, timeout=180)
        print("Approved.")
        time.sleep(3)

    deadline = int(time.time()) + 300
    swap_tx = router.functions.swapExactTokensForETH(
        sell_raw, min_out, path, addr, deadline
    ).build_transaction({
        "from": addr, "value": 0,
        "nonce": w3.eth.get_transaction_count(addr),
        "chainId": POLYGON_CHAIN_ID, "gasPrice": gas_price,
    })
    try:
        g = w3.eth.estimate_gas(swap_tx)
        swap_tx["gas"] = int(g * 1.3)
    except:
        swap_tx["gas"] = 250000

    print("Signing and broadcasting swap...")
    signed = w3.eth.account.sign_transaction(swap_tx, private_key=pk)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"TX: {tx_hash.hex()}")
    print(f"https://polygonscan.com/tx/0x{tx_hash.hex()}")

    print("Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt.get("status") == 1:
        print("Swap confirmed!")
    else:
        sys.exit("Swap FAILED")

    time.sleep(2)
    new_pol = w3.eth.get_balance(addr) / 1e18
    new_usdc = usdc.functions.balanceOf(addr).call() / 1e6
    print(f"\nNew POL:  {new_pol:.6f}")
    print(f"New USDC: {new_usdc:.6f}")

if __name__ == "__main__":
    main()
