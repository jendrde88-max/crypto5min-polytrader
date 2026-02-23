"""Inspect trades with redeem_status='submitted' in poly_trades.json.

Run inside container: python /app/inspect_submitted_redeems.py
"""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    p = Path('/app/logs/poly_trades.json')
    trades = json.loads(p.read_text()) if p.exists() else []
    trades = [t for t in trades if isinstance(t, dict)]

    submitted = [t for t in trades if t.get('redeem_status') == 'submitted']
    print('submitted_count', len(submitted))

    for t in submitted[-15:]:
        txh = t.get('redeem_tx_hash')
        txs = str(txh) if txh is not None else ''
        txs_clean = txs.strip()
        print('---')
        print('window_slug', t.get('window_slug'))
        print('redeem_tx_hash_raw', repr(txs))
        print('redeem_tx_hash_stripped', repr(txs_clean))
        print('len_stripped', len(txs_clean))
        print('starts_0x', txs_clean.startswith('0x'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
