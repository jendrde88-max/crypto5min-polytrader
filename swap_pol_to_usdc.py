#!/usr/bin/env python3
"""
Swap POL (native Polygon token) → USDC.e via QuickSwap V2 Router.

No external API key needed — swaps directly on-chain via QuickSwap DEX.

Usage:
    python tools/swap_pol_to_usdc.py [--amount POL_AMOUNT] [--dry-run]

If --amount is omitted, swaps all POL minus a 0.15 POL reserve for gas.
"""
from __future__ import annotations

import argparse
import os
import sys
import time

from web3 import Web3

# ── constants ────────────────────────────────────────────────────────
POLYGON_CHAIN_ID = 137
USDC_E_POLYGON = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
WMATIC = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
QUICKSWAP_ROUTER = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
GAS_RESERVE_POL = 0.15  # keep for future gas
SLIPPAGE_BPS = 200      # 2% slippage tolerance

_ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]

# Uniswap V2 Router ABI (only the functions we need)
_ROUTER_ABI = [
    {
        "name": "getAmountsOut",
        "type": "function",
        "stateMutability": "view",
        "inputs": [
            {"name": "amountIn", "type": "uint256"},
            {"name": "path", "type": "address[]"},
        ],
        "outputs": [
            {"name": "amounts", "type": "uint256[]"},
        ],
    },
    {
        "name": "swapExactETHForTokens",
        "type": "function",
        "stateMutability": "payable",
        "inputs": [
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "path", "type": "address[]"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"},
        ],
        "outputs": [
            {"name": "amounts", "type": "uint256[]"},
        ],
    },
]


def _env(key: str, default: str | None = None) -> str:
    val = os.getenv(key, default)
    if val is None:
        sys.exit(f"ERROR: env var {key} is not set")
    return val


def main() -> None:
    parser = argparse.ArgumentParser(description="Swap POL → USDC.e on Polygon via QuickSwap")
    parser.add_argument("--amount", type=float, default=None,
                        help="Amount of POL to swap (default: all minus reserve)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only show quote, do not execute swap")
    args = parser.parse_args()

    # ── env vars ─────────────────────────────────────────────────────
    private_key = _env("C5_POLY_PRIVATE_KEY")
    rpc_url = _env("C5_POLYGON_RPC", "https://polygon-bor-rpc.publicnode.com")

    # ── web3 setup ───────────────────────────────────────────────────
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        sys.exit("ERROR: cannot connect to Polygon RPC")

    acct = w3.eth.account.from_key(private_key)
    addr = acct.address
    print(f"Wallet: {addr}")

    # ── contracts ────────────────────────────────────────────────────
    usdc_addr = Web3.to_checksum_address(USDC_E_POLYGON)
    wmatic_addr = Web3.to_checksum_address(WMATIC)
    router_addr = Web3.to_checksum_address(QUICKSWAP_ROUTER)

    usdc_contract = w3.eth.contract(address=usdc_addr, abi=_ERC20_ABI)
    router = w3.eth.contract(address=router_addr, abi=_ROUTER_ABI)

    # ── current balances ─────────────────────────────────────────────
    pol_wei = w3.eth.get_balance(addr)
    pol_balance = pol_wei / 1e18

    usdc_raw = usdc_contract.functions.balanceOf(addr).call()
    usdc_balance = usdc_raw / 1e6

    print(f"POL  balance: {pol_balance:.6f}")
    print(f"USDC balance: {usdc_balance:.6f}")

    # ── how much to swap ─────────────────────────────────────────────
    if args.amount is not None:
        sell_pol = args.amount
    else:
        sell_pol = pol_balance - GAS_RESERVE_POL

    if sell_pol <= 0.01:
        sys.exit(f"ERROR: not enough POL to swap (available after reserve: {sell_pol:.6f})")

    sell_wei = int(sell_pol * 1e18)
    print(f"\nSwapping {sell_pol:.6f} POL -> USDC.e  (keeping {GAS_RESERVE_POL} POL for gas)")

    # ── get quote via router ─────────────────────────────────────────
    path = [wmatic_addr, usdc_addr]
    amounts_out = router.functions.getAmountsOut(sell_wei, path).call()
    expected_usdc_raw = amounts_out[1]
    expected_usdc = expected_usdc_raw / 1e6

    # apply slippage
    min_out = int(expected_usdc_raw * (10000 - SLIPPAGE_BPS) / 10000)
    min_out_usdc = min_out / 1e6

    print(f"Quote: {sell_pol:.6f} POL -> ~{expected_usdc:.6f} USDC.e")
    print(f"Min output (with {SLIPPAGE_BPS/100:.1f}% slippage): {min_out_usdc:.6f} USDC.e")

    if args.dry_run:
        print("\n[DRY RUN] -- not executing swap")
        return

    # ── build & send swap tx ─────────────────────────────────────────
    deadline = int(time.time()) + 300  # 5 minutes

    swap_tx = router.functions.swapExactETHForTokens(
        min_out,
        path,
        addr,
        deadline,
    ).build_transaction({
        "from": addr,
        "value": sell_wei,
        "nonce": w3.eth.get_transaction_count(addr),
        "chainId": POLYGON_CHAIN_ID,
        "gasPrice": w3.eth.gas_price,
    })

    # estimate gas
    try:
        gas_est = w3.eth.estimate_gas(swap_tx)
        swap_tx["gas"] = int(gas_est * 1.3)
    except Exception as e:
        print(f"Gas estimation warning: {e}")
        swap_tx["gas"] = 250_000

    gas_gwei = swap_tx["gasPrice"] / 1e9
    print(f"Gas price: {gas_gwei:.2f} gwei, gas limit: {swap_tx['gas']}")
    print("Signing and broadcasting...")

    signed = w3.eth.account.sign_transaction(swap_tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    tx_hash_hex = tx_hash.hex()
    print(f"TX sent: {tx_hash_hex}")
    print(f"https://polygonscan.com/tx/0x{tx_hash_hex}")

    # ── wait for receipt ─────────────────────────────────────────────
    print("Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    status = receipt.get("status", 0)
    if status == 1:
        print("Swap confirmed!")
    else:
        print(f"Swap FAILED (status={status})")
        sys.exit(1)

    # ── final balances ───────────────────────────────────────────────
    time.sleep(2)
    new_pol = w3.eth.get_balance(addr) / 1e18
    new_usdc = usdc_contract.functions.balanceOf(addr).call() / 1e6
    print(f"\nNew POL  balance: {new_pol:.6f}")
    print(f"New USDC balance: {new_usdc:.6f}")


if __name__ == "__main__":
    main()
