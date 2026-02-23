"""Print a fresh Polymarket account snapshot.

Run this *inside* the container so dependencies are available, and load env from
/app/config/.env (mounted).

This script does NOT print private keys.
"""

from __future__ import annotations

import json
import os
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
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
            v = v[1:-1]
        os.environ[k] = v


def main() -> int:
    _load_env_file('/app/config/.env')

    from crypto5min_polytrader.polymarket_account import snapshot_from_env

    snap = snapshot_from_env()
    if not snap:
        print(json.dumps({'ok': False, 'error': 'no_snapshot'}, indent=2))
        return 1

    d = snap.as_dict()
    # Add a couple safe env flags for debugging.
    d['_env_safe'] = {
        'mode': os.getenv('C5_MODE', ''),
        'dry_run': os.getenv('C5_POLY_DRY_RUN', ''),
        'signature_type': os.getenv('C5_POLY_SIGNATURE_TYPE', ''),
        'has_funder': bool(os.getenv('C5_POLY_FUNDER_ADDRESS')),
        'has_private_key': bool(os.getenv('C5_POLY_PRIVATE_KEY')),
    }
    print(json.dumps(d, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
