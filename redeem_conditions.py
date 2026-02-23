"""Redeem resolved Polymarket positions by conditionId.

This is an operator convenience script meant to be run *inside* the Docker
container (so it has access to installed deps and the mounted /app/config/.env).

It does NOT print secrets.

Usage (inside container):
  python /tmp/redeem_conditions.py --condition-id 0x... --condition-id 0x...
  python /tmp/redeem_conditions.py --dry-run --condition-id 0x...
"""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path


def _load_env_file(path: str) -> None:
    p = Path(path)
    if not p.exists():
        return
    for ln in p.read_text(encoding='utf-8', errors='ignore').splitlines():
        s = ln.strip()
        if not s or s.startswith('#') or '=' not in s:
            continue
        k, v = s.split('=', 1)
        k = k.strip()
        v = v.strip()
        # Strip surrounding quotes (matches python-dotenv behaviour).
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
            v = v[1:-1]
        os.environ[k] = v


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='Plan only; do not broadcast tx')
    ap.add_argument('--condition-id', action='append', default=[], help='0x… conditionId (repeatable)')
    ap.add_argument('--sleep-sec', type=float, default=2.0, help='Delay between tx submissions')
    args = ap.parse_args()

    cids = [str(x).strip() for x in (args.condition_id or []) if str(x).strip()]
    if not cids:
        print('error: at least one --condition-id is required')
        return 2

    # Load mounted env file (preferred by the app).
    _load_env_file('/app/config/.env')

    # Print only safe env diagnostics.
    rpc = (os.getenv('C5_POLYGON_RPC', '') or 'https://polygon-bor-rpc.publicnode.com').strip()
    print('redeem_env_safe=', {
        'has_private_key': bool(os.getenv('C5_POLY_PRIVATE_KEY')),
        'signature_type': os.getenv('C5_POLY_SIGNATURE_TYPE', ''),
        'has_funder': bool(os.getenv('C5_POLY_FUNDER_ADDRESS')),
        'rpc_prefix': (rpc[:40] + '…') if rpc else '',
        'dry_run': bool(args.dry_run),
        'count': len(cids),
    })

    from crypto5min_polytrader.polymarket_redeem import redeem_positions_for_trade

    for i, cid in enumerate(cids, start=1):
        trade = {'condition_id': cid}
        res = redeem_positions_for_trade(trade=trade, dry_run=bool(args.dry_run))
        print('redeem_result', i, {
            'ok': res.get('ok'),
            'condition_id': res.get('condition_id') or cid,
            'tx_hash': res.get('tx_hash'),
            'error': res.get('error'),
        })
        if i < len(cids):
            time.sleep(max(0.0, float(args.sleep_sec)))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
