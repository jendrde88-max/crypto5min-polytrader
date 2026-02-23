"""VPS helper: extract a Windows-created ZIP on Linux.

Some zips created on Windows can contain entries with backslashes (e.g.
"templates\\dashboard.html") instead of POSIX separators.

This script extracts a ZIP into an output directory while normalizing
path separators to '/' and preventing path traversal.

Usage (on VPS):
  python3 vps_extract_zip.py /path/to/file.zip /path/to/out_dir

"""

from __future__ import annotations

import os
import sys
import zipfile
from pathlib import PurePosixPath


def _safe_relpath(name: str) -> PurePosixPath | None:
    name = (name or '').replace('\\', '/')
    if (not name) or name.endswith('/'):
        return None
    p = PurePosixPath(name)
    if p.is_absolute() or ('..' in p.parts):
        return None
    return p


def extract(zip_path: str, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            p = _safe_relpath(info.filename)
            if p is None:
                continue
            dest = os.path.join(out_dir, *p.parts)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(info, 'r') as src, open(dest, 'wb') as dst:
                dst.write(src.read())


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print('usage: python3 vps_extract_zip.py ZIP_PATH OUT_DIR')
        return 2
    zip_path, out_dir = argv[1], argv[2]
    extract(zip_path, out_dir)
    print('extracted_ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
