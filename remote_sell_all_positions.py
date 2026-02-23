"""Remote helper: cancel open orders and place SELL orders for all positions.

This script is designed to be copied to a server and executed inside a container
that has the Polymarket bot code + dependencies.

It does NOT contain any secrets. It reads configuration from the container env
and/or its .env file.

Notes:
- This places limit SELL orders. Fills are not guaranteed.
- It cancels existing LIVE orders first.
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any


def _to_f(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def main() -> int:
    # Common layouts:
    # - app code in /app/src with polymarket.py
    for p in ("/app/src", "/app"):
        if p not in sys.path:
            sys.path.insert(0, p)

    try:
        # Prefer src.polymarket if it exists.
        from src.polymarket import PolyInterface  # type: ignore
    except Exception:
        from polymarket import PolyInterface  # type: ignore

    # Best-effort load .env
    try:
        from dotenv import load_dotenv  # type: ignore

        for env_path in ("/app/.env", "/app/config/.env", ".env"):
            if os.path.exists(env_path):
                load_dotenv(env_path, override=True)
                break
    except Exception:
        pass

    slip = _to_f(os.getenv("SELL_ALL_SLIP", "0.02"), 0.02)
    slip = max(0.0, min(0.20, abs(slip)))

    poly = PolyInterface()

    addr = getattr(poly, "address", None)
    print(f"address={addr}")

    # Cancel open LIVE orders
    try:
        open_orders = poly.get_open_orders() or []
    except Exception as e:
        print(f"open_orders_error={e}")
        open_orders = []

    live_ids = []
    for o in open_orders:
        try:
            if str(o.get("status", "")).upper() == "LIVE":
                oid = o.get("id")
                if oid:
                    live_ids.append(oid)
        except Exception:
            continue

    print(f"open_orders={len(open_orders)} live_orders={len(live_ids)}")
    if live_ids:
        try:
            res = poly.cancel_orders(live_ids)
            print(f"cancel_result={res}")
        except Exception as e:
            print(f"cancel_error={e}")

    # Place SELL orders for all positions
    try:
        positions = poly.get_my_positions() or []
    except Exception as e:
        print(f"positions_error={e}")
        positions = []

    placed = 0
    failed = 0
    skipped = 0
    skipped_zero = 0

    start = time.time()
    for p in positions:
        try:
            size = _to_f(p.get("size", 0), 0.0)
            if size <= 0:
                continue
            token_id = str(p.get("asset") or "").strip()
            if not token_id:
                skipped += 1
                continue
            cur = _to_f(p.get("curPrice", 0), 0.0)
            if cur <= 0:
                skipped_zero += 1
                continue

            # Prefer best bid from order book (if available)
            best_bid = None
            try:
                ob = poly.get_order_book(token_id)
                bids = getattr(ob, "bids", None) if ob else None
                bids = bids or []
                if bids:
                    best_bid = max(_to_f(getattr(b, "price", None), 0.0) for b in bids)
                    if not best_bid or best_bid <= 0:
                        best_bid = None
            except Exception:
                best_bid = None

            if best_bid:
                # To get filled, set <= best bid.
                price = best_bid * (1.0 - min(0.01, slip))
            else:
                price = cur * (1.0 - slip)

            price = max(0.01, min(0.99, float(price)))

            # Place SELL
            from py_clob_client.order_builder.constants import SELL  # type: ignore

            r = poly.post_order(token_id=token_id, side=SELL, price=price, size=float(size))
            if isinstance(r, dict) and r.get("ok"):
                placed += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    dur_ms = int((time.time() - start) * 1000)

    # Report balances
    try:
        usdc = poly.get_usdc_balance()
    except Exception:
        usdc = None

    print(
        {
            "ok": True,
            "positions_seen": len(positions),
            "sell_orders_placed": placed,
            "sell_orders_failed": failed,
            "skipped_missing": skipped,
            "skipped_zero_price": skipped_zero,
            "duration_ms": dur_ms,
            "usdc_balance": usdc,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
