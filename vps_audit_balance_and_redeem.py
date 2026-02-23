"""Audit Polymarket balance/positions vs redeem state.

Intended to run INSIDE the app container (where /app/src is on PYTHONPATH).
This script prints:
- snapshot_from_env: equity, clob (cash), positions value, open_positions
- redeem candidates count
- count of wins that are not marked redeem_status=success

No secrets are printed (it does not dump env vars).
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def main() -> int:
    # Load container env-config.
    try:
        from dotenv import load_dotenv

        load_dotenv('/app/config/.env')
    except Exception as e:
        print('WARN: could not load /app/config/.env via python-dotenv:', e)

    # Snapshot (CLOB cash + positions value).
    try:
        from crypto5min_polytrader.polymarket_account import snapshot_from_env

        snap = snapshot_from_env() or {}
        print('SNAPSHOT')
        # snapshot_from_env returns a PolyAccountSnapshot dataclass.
        # We also support dicts here for robustness.
        def _g(obj, key, default=None):
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        clob = _g(snap, 'clob_balance_usdc', 0.0)
        pos = _g(snap, 'positions_value_usdc', 0.0)
        total = _g(snap, 'total_equity_usdc', None)
        if total is None:
            try:
                total = float(clob) + float(pos)
            except Exception:
                total = None

        print('  address:', _g(snap, 'address'))
        print('  total_equity_usdc:', total)
        print('  clob_balance_usdc:', clob)
        print('  positions_value_usdc:', pos)
        print('  cost_basis_usdc:', _g(snap, 'cost_basis_usdc'))
        print('  unrealized_pnl_usdc:', _g(snap, 'unrealized_pnl_usdc'))
        print('  active_positions:', _g(snap, 'active_positions'))
        print('  native_gas_balance:', _g(snap, 'native_gas_symbol'), _g(snap, 'native_gas_balance'))
    except Exception as e:
        print('ERROR: snapshot_from_env failed:', e)
        snap = {}

    # Redeem candidates (what the bot considers claimable wins).
    try:
        from crypto5min_polytrader import polymarket_redeem as redeem

        res = redeem.find_redeem_candidates(max_trades=50) or {}
        candidates = res.get('candidates') if isinstance(res, dict) else None
        candidates_list = candidates if isinstance(candidates, list) else []
        n = len(candidates_list)
        print('REDEEM_CANDIDATES')
        print('  count:', n)
        if n:
            # show first few candidate indices/slugs
            for it in candidates_list[:5]:
                if isinstance(it, dict):
                    print('  -', it.get('trade_index'), it.get('window_slug'), it.get('reason') or '')
                else:
                    print('  -', str(it)[:200])
    except Exception as e:
        print('ERROR: find_redeem_candidates failed:', e)

    # Trades log: resolved wins and redeem_status distribution.
    try:
        p = Path('/app/logs/poly_trades.json')
        trades = json.loads(p.read_text()) if p.exists() else []
        trades = [t for t in trades if isinstance(t, dict)]
        wins = [t for t in trades if t.get('resolved') == 'win']
        losses = [t for t in trades if t.get('resolved') == 'loss']

        rs = Counter((t.get('redeem_status') or '') for t in wins)
        not_success = [t for t in wins if t.get('redeem_status') != 'success']

        print('TRADES')
        print('  total:', len(trades))
        print('  wins:', len(wins))
        print('  losses:', len(losses))
        print('  win_redeem_status:', dict(rs))
        print('  wins_not_success:', len(not_success))
        if not_success:
            print('  sample_not_success:')
            for t in not_success[-5:]:
                print('   -', t.get('window_slug'), t.get('redeem_status'), t.get('redeem_tx_hash'))
    except Exception as e:
        print('ERROR: poly_trades.json audit failed:', e)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
