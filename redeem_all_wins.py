"""Force-run on-chain redemption for all eligible winning Polymarket trades.

This is an ops script (intended to run on the server). It:
- loads config/.env
- finds redeem candidates from logs/poly_trades.json
- submits redeem txs (live) in batches
- attempts a best-effort receipt reconciliation

Use with care: this sends real on-chain transactions and costs gas.
"""

from __future__ import annotations

import json
import time
from typing import Any

from dotenv import load_dotenv


def _pp(x: Any) -> str:
    try:
        return json.dumps(x, indent=2, sort_keys=True)[:5000]
    except Exception:
        return str(x)[:5000]


def main() -> int:
    load_dotenv('config/.env')

    from crypto5min_polytrader import polymarket_redeem as redeem

    # Loop a few times to drain the queue.
    max_rounds = 6
    total_submitted = 0

    for r in range(1, max_rounds + 1):
        c = redeem.find_redeem_candidates(max_trades=50)
        candidates = c.get('candidates') if isinstance(c, dict) else None
        n = len(candidates) if isinstance(candidates, list) else 0
        print(f'\n=== round {r}/{max_rounds}: candidates={n}')
        if n == 0:
            break

        res = redeem.process_auto_redeem(dry_run=False)
        print('process_auto_redeem:', _pp(res))

        # process_auto_redeem returns a list of per-trade results; count the ok ones.
        submitted = 0
        if isinstance(res, dict) and isinstance(res.get('results'), list):
            for it in res['results']:
                if isinstance(it, dict) and it.get('ok') and it.get('tx_hash'):
                    submitted += 1
        total_submitted += submitted

        # Give the network a moment; many txs won't be mined immediately.
        time.sleep(3)

        rec = redeem.reconcile_redeem_txs(max_trades=50)
        print('reconcile_redeem_txs:', _pp(rec))

        # If we didn't submit anything new, don't spin forever.
        if submitted == 0:
            break

    print(f'\nDONE: total_submitted={total_submitted}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
