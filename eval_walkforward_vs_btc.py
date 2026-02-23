#!/usr/bin/env python3
"""Evaluate the model over many windows (walk-forward refit) using the same backtest pipeline.

This is the "all windows" counterpart to tools/eval_trades_vs_btc.py.

It:
- loads cached Coinbase candles CSV
- computes features via crypto5min_polytrader.features.add_features
- computes walk-forward-ish probabilities using crypto5min_polytrader.runner._walk_forward_probs
  (periodic refit with fast logistic regression; same as runner.run_once backtest)
- evaluates probability quality and directional accuracy

Important:
- features.add_features applies a deadband on the training label y_up and drops rows
  inside that deadband. This evaluation therefore covers the same subset of windows the
  model is trained on (noise-filtered moves).
- We score outcomes using close-to-close for the next candle via future_close > close.

Outputs:
- summary printed to stdout
- optional per-row CSV + JSON report
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def _add_repo_src_to_syspath() -> None:
    # tools/ is at repo_root/tools/, so repo root is parent.
    root = Path(__file__).resolve().parents[1]
    src = root / 'src'
    if src.exists():
        sys.path.insert(0, str(src))


def _bucket_label(p: float, bucket: float) -> str:
    lo = math.floor(p / bucket) * bucket
    hi = lo + bucket
    return f'{lo:.2f}-{hi:.2f}'


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def main() -> int:
    ap = argparse.ArgumentParser(description='Walk-forward evaluation over candle history')
    ap.add_argument('--candles', default='data/candles_BTC-USD_300.csv', help='Candles CSV path')
    ap.add_argument('--min-train', type=int, default=300, help='Minimum training rows before scoring (default 300)')
    ap.add_argument('--refit-every', type=int, default=12, help='Refit cadence in rows (default 12 = 1h at 5m)')
    ap.add_argument('--max-train', type=int, default=2000, help='Max rolling train rows (default 2000)')
    ap.add_argument('--bucket', type=float, default=0.05, help='Calibration bucket size (default 0.05)')
    ap.add_argument('--out-csv', default='logs/eval_walkforward_rows.csv', help='Write per-row CSV (empty to disable)')
    ap.add_argument('--out-json', default='logs/eval_walkforward_report.json', help='Write JSON report (empty to disable)')

    args = ap.parse_args()

    candles_path = Path(args.candles)
    if not candles_path.exists():
        raise SystemExit(f'Candles file not found: {candles_path}')

    _add_repo_src_to_syspath()

    import pandas as pd  # type: ignore

    from crypto5min_polytrader.features import add_features
    from crypto5min_polytrader.runner import _walk_forward_probs

    df = pd.read_csv(candles_path)
    if df.empty:
        raise SystemExit('Candles CSV is empty')

    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], utc=True, errors='coerce')

    feats = add_features(df)
    if feats.empty or len(feats) < (args.min_train + 10):
        raise SystemExit(f'Not enough feature rows for evaluation: {len(feats)}')

    # True outcome for the next 5-min candle (close-to-close)
    # future_close exists in feats.
    feats = feats.sort_values('time').reset_index(drop=True)
    y_true = (feats['future_close'].astype(float) > feats['close'].astype(float)).astype(int)

    probs = _walk_forward_probs(
        feats,
        min_train=int(args.min_train),
        refit_every=int(args.refit_every),
        max_train=int(args.max_train),
    )

    if len(probs) != len(feats):
        raise SystemExit(f'Internal error: probs len {len(probs)} != feats len {len(feats)}')

    # Build evaluatable rows
    rows: List[Dict[str, Any]] = []
    for i, p in enumerate(probs):
        if p is None:
            continue
        p_up = float(p)
        if not (0.0 <= p_up <= 1.0) or not math.isfinite(p_up):
            continue

        y = int(y_true.iloc[i])
        direction = 'UP' if p_up >= 0.5 else 'DOWN'
        confidence = p_up if direction == 'UP' else 1.0 - p_up
        correct = 1 if ((direction == 'UP' and y == 1) or (direction == 'DOWN' and y == 0)) else 0
        brier = (p_up - float(y)) ** 2

        rows.append(
            {
                'time': str(feats.iloc[i]['time']) if 'time' in feats.columns else str(i),
                'p_up': p_up,
                'direction': direction,
                'confidence': confidence,
                'y_up': y,
                'correct': correct,
                'brier': brier,
            }
        )

    n = len(rows)
    if n == 0:
        raise SystemExit('No evaluatable rows (all probs were None?)')

    accuracy = sum(r['correct'] for r in rows) / n
    brier_mean = statistics.mean(r['brier'] for r in rows)

    # Calibration by confidence bucket
    bucket = float(args.bucket)
    calib: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        lbl = _bucket_label(float(r['confidence']), bucket)
        b = calib.setdefault(lbl, {'n': 0, 'wins': 0, 'avg_conf': 0.0})
        b['n'] += 1
        b['wins'] += int(r['correct'])
        b['avg_conf'] += float(r['confidence'])

    for lbl, b in calib.items():
        b['win_rate'] = (b['wins'] / b['n']) if b['n'] else None
        b['avg_conf'] = (b['avg_conf'] / b['n']) if b['n'] else None

    report = {
        'candles_file': str(candles_path),
        'n_rows_scored': n,
        'min_train': int(args.min_train),
        'refit_every': int(args.refit_every),
        'max_train': int(args.max_train),
        'accuracy': accuracy,
        'brier': brier_mean,
        'calibration': dict(sorted(calib.items(), key=lambda kv: kv[0])),
    }

    print('=== Walk-forward sanity report ===')
    print(f'Rows scored: {n}')
    print(f'Accuracy: {accuracy:.3f}')
    print(f'Brier: {brier_mean:.4f} (lower is better)')

    print('\nCalibration (by confidence bucket):')
    for lbl, b in report['calibration'].items():
        print(f"  {lbl}: n={b['n']:5d} win_rate={b['win_rate']:.3f} avg_conf={b['avg_conf']:.3f}")

    if args.out_csv:
        out_csv = Path(args.out_csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        with out_csv.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f'\nWrote rows CSV: {out_csv}')

    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
        print(f'Wrote report JSON: {out_json}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
