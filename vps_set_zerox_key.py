"""VPS helper: set 0x API key and enable gas top-up.

Reads key from env var ZEROX_API_KEY and updates a config/.env file.
Does not print the key.

Usage (on VPS):
  ENVF=/path/to/config/.env ZEROX_API_KEY=... python3 vps_set_zerox_key.py

"""

from __future__ import annotations

import os
from pathlib import Path


def main() -> int:
    envf = Path(os.environ.get('ENVF', '')).expanduser()
    api_key = (os.environ.get('ZEROX_API_KEY') or '').strip()

    if not str(envf):
        print('error: ENVF not set')
        return 2
    if not envf.exists():
        print('error: env file not found')
        return 2
    if not api_key:
        print('error: ZEROX_API_KEY missing')
        return 2

    lines = envf.read_text(errors='ignore').splitlines()
    out: list[str] = []
    seen_key = False
    seen_enabled = False

    for ln in lines:
        if ln.startswith('C5_ZEROX_API_KEY='):
            out.append('C5_ZEROX_API_KEY=' + api_key)
            seen_key = True
            continue
        if ln.startswith('C5_GAS_TOPUP_ENABLED='):
            out.append('C5_GAS_TOPUP_ENABLED=true')
            seen_enabled = True
            continue
        out.append(ln)

    if not seen_key:
        out.append('C5_ZEROX_API_KEY=' + api_key)
    if not seen_enabled:
        out.append('C5_GAS_TOPUP_ENABLED=true')

    envf.write_text('\n'.join(out).rstrip() + '\n', encoding='utf-8')
    print('updated_env_ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
