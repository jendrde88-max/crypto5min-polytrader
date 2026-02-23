#!/usr/bin/env python3
"""Identify the 5 open positions and cross-reference with trades log."""
import json, requests, sys

WALLET = "0xf8764f91A3b8f6bF111e9EC5c670B541415D8975"

# Load trades
try:
    with open("/app/logs/poly_trades.json") as f:
        trades = json.load(f)
    print(f"Trades in log: {len(trades)}")
except Exception as e:
    trades = []
    print(f"Error loading trades: {e}")

# Build lookup by condition_id
trades_by_cid = {t.get("condition_id", ""): t for t in trades if t.get("condition_id")}

# Fetch all positions
resp = requests.get(
    f"https://data-api.polymarket.com/positions?user={WALLET}&limit=500&sizeThreshold=0.01",
    timeout=30
)
positions = resp.json() if resp.status_code == 200 else []
print(f"API positions (size>0.01): {len(positions)}")

live = [p for p in positions if float(p.get("currentValue", 0)) > 0]
print(f"\n=== {len(live)} LIVE POSITIONS (currentValue > $0) ===\n")

for p in live:
    cid = p.get("conditionId", "")
    title = (p.get("title") or p.get("market") or "")[:60]
    val = float(p.get("currentValue", 0))
    size = float(p.get("size", 0))
    redeemable = p.get("redeemable", False)
    outcome = p.get("outcome", "?")
    token_id = p.get("asset", p.get("tokenId", ""))

    print(f"  [{outcome}] {title}")
    print(f"    Value=${val:.4f}  Size={size:.2f}  Redeemable={redeemable}")
    print(f"    conditionId={cid}")
    print(f"    tokenId={token_id}")

    match = trades_by_cid.get(cid)
    if match:
        status = match.get("order_status", "?")
        resolved = match.get("resolved", None)
        redeem_tx = match.get("redeem_tx_hash", "")
        usdc = match.get("usdc", "?")
        slug = match.get("window_slug", "?")
        placed_ts = match.get("placed_ts", "?")
        print(f"    TRADE MATCH: slug={slug} usdc={usdc} status={status} resolved={resolved}")
        if redeem_tx:
            print(f"    redeem_tx={redeem_tx[:40]}")
    else:
        print(f"    *** NO TRADE MATCH - ORPHAN POSITION ***")
    print()

# Show trades that are filled but not resolved (should be 0 based on earlier check)
pending = [t for t in trades if t.get("order_status") == "filled" and not t.get("resolved") and not t.get("redeem_tx_hash")]
print(f"\n=== FILLED BUT UNRESOLVED TRADES: {len(pending)} ===")
for t in pending:
    print(f"  {t.get('window_slug')} | usdc={t.get('usdc')} | cid={t.get('condition_id','')[:20]}...")

# Show all redeemable positions sorted by value
all_redeemable = [p for p in positions if p.get("redeemable") and float(p.get("currentValue", 0)) > 0]
print(f"\nTotal redeemable WITH value > 0: {len(all_redeemable)}")

# Live CLOB balance
print("\n=== LIVE CLOB BALANCE ===")
try:
    from crypto5min_polytrader.polymarket_exec import clob_balance_usdc
    import asyncio
    bal = asyncio.run(clob_balance_usdc())
    print(f"  CLOB: ${bal:.4f}")
except Exception as e:
    print(f"  Error: {e}")

print("\nDone.")
