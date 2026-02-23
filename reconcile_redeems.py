"""Best-effort reconcile of submitted redeem transactions.

Run this inside the app container (or on the host with same env) to mark
redeem_status=submitted -> success/failed once txs are mined.

This does NOT submit new transactions.
"""

from __future__ import annotations

from dotenv import load_dotenv


def main() -> int:
    load_dotenv('config/.env')

    from crypto5min_polytrader import polymarket_redeem as r

    res = r.reconcile_redeem_txs(max_trades=100)
    print(res)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
