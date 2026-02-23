#!/usr/bin/env python3
"""Evaluate whether traded predictions "add up" vs realized BTC 5-minute moves.

This script cross-references:
- Polymarket trade log records (default: logs/poly_trades.json)
- Coinbase candle history (default: data/candles_BTC-USD_300.csv)

For each traded window (each trade record with a valid window_slug), it:
- parses window start_ts from window_slug (e.g. btc-updown-5m-1771194900)
- computes realized UP/DOWN for that 5-min window using close-to-close:
    realized_up := close(t=start_ts) > close(t=start_ts - granularity)
- computes probability scores:
    p_up reconstructed from trade's (direction, confidence)
    brier := (p_up - y)^2 where y=1 for realized_up else 0
- computes edge vs market price (for the chosen direction):
    edge := confidence - price

Outputs:
- prints a summary
- optionally writes per-trade rows CSV and a JSON report

Notes:
- This evaluates *traded windows only* (not every 5-min window).
- Candle source is Coinbase; Polymarket resolves using an index. Expect some noise.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import statistics
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


WINDOW_SLUG_RE = re.compile(r".*-(\d{9,12})$")


def _parse_window_start_ts(window_slug: str) -> Optional[int]:
    """Extract start_ts (unix seconds) from a window slug."""
    if not window_slug or not isinstance(window_slug, str):
        return None
    m = WINDOW_SLUG_RE.match(window_slug.strip())
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def _safe_float(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None


def _safe_bool(x: Any) -> Optional[bool]:
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        return bool(x)
    if isinstance(x, str):
        v = x.strip().lower()
        if v in {"true", "t", "1", "yes", "y"}:
            return True
        if v in {"false", "f", "0", "no", "n"}:
            return False
    return None


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _read_candles_close_by_ts(candles_csv: Path) -> Dict[int, float]:
    """Load candles CSV and return mapping unix_ts -> close.

    The CSV is expected to have columns: time, low, high, open, close, volume.
    The time column may be ISO (timezone-aware) or epoch seconds.

    We map each row to unix seconds (UTC) and keep the last close for each ts.
    """
    close_by_ts: Dict[int, float] = {}

    with candles_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise RuntimeError(f"No columns found in {candles_csv}")
        if "time" not in reader.fieldnames or "close" not in reader.fieldnames:
            raise RuntimeError(
                f"Expected columns time, close in {candles_csv}; got {reader.fieldnames}"
            )

        for row in reader:
            t_raw = row.get("time")
            c_raw = row.get("close")
            if t_raw is None or c_raw is None:
                continue

            # parse time
            ts: Optional[int] = None
            # epoch seconds?
            try:
                if isinstance(t_raw, str) and t_raw.strip().isdigit():
                    ts = int(t_raw.strip())
                else:
                    # ISO-ish
                    dt = datetime.fromisoformat(str(t_raw).strip())
                    if dt.tzinfo is None:
                        # assume UTC
                        ts = int(dt.replace(tzinfo=datetime.now().astimezone().tzinfo).timestamp())
                    else:
                        ts = int(dt.timestamp())
            except Exception:
                # last resort: try float seconds
                try:
                    ts = int(float(str(t_raw).strip()))
                except Exception:
                    ts = None

            close = _safe_float(c_raw)
            if ts is None or close is None or not math.isfinite(close):
                continue

            close_by_ts[ts] = float(close)

    return close_by_ts


def _realized_up(close_by_ts: Dict[int, float], start_ts: int, granularity: int) -> Optional[bool]:
    """Return True/False for realized UP, or None if candles missing."""
    c_prev = close_by_ts.get(start_ts - granularity)
    c_now = close_by_ts.get(start_ts)
    if c_prev is None or c_now is None:
        return None
    return bool(c_now > c_prev)


def _p_up_from_trade(direction: str, confidence: float) -> Optional[float]:
    direction = (direction or "").strip().upper()
    if direction not in {"UP", "DOWN"}:
        return None
    if not (0.0 <= confidence <= 1.0):
        return None
    return confidence if direction == "UP" else 1.0 - confidence


@dataclass
class Row:
    window_slug: str
    start_ts: int
    direction: str
    confidence: float
    price: Optional[float]
    usdc: Optional[float]
    realized_up: bool
    correct: bool
    p_up: float
    brier: float
    edge_vs_price: Optional[float]


def _bucket_label(p: float, bucket: float) -> str:
    # e.g., bucket=0.05; p=0.547 => 0.55-0.60 (rounding down)
    lo = math.floor(p / bucket) * bucket
    hi = lo + bucket
    return f"{lo:.2f}-{hi:.2f}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Cross-check traded predictions vs realized BTC 5m moves")
    ap.add_argument("--trades", default="logs/poly_trades.json", help="Path to poly_trades.json")
    ap.add_argument("--candles", default="data/candles_BTC-USD_300.csv", help="Path to candles CSV")
    ap.add_argument("--granularity", type=int, default=300, help="Candle/window size in seconds (default 300)")
    ap.add_argument("--bucket", type=float, default=0.05, help="Calibration bucket size (default 0.05)")
    ap.add_argument("--out-csv", default="logs/eval_trades_rows.csv", help="Write per-trade rows CSV (set empty to disable)")
    ap.add_argument("--out-json", default="logs/eval_trades_report.json", help="Write summary JSON report (set empty to disable)")

    args = ap.parse_args()

    trades_path = Path(args.trades)
    candles_path = Path(args.candles)
    if not trades_path.exists():
        raise SystemExit(f"Trades file not found: {trades_path}")
    if not candles_path.exists():
        raise SystemExit(f"Candles file not found: {candles_path}")

    trades = _load_json(trades_path, default=[])
    if not isinstance(trades, list):
        raise SystemExit(f"Expected a JSON list in {trades_path}")

    close_by_ts = _read_candles_close_by_ts(candles_path)

    rows: List[Row] = []
    skipped: Dict[str, int] = {
        "missing_window_slug": 0,
        "bad_window_slug": 0,
        "missing_direction": 0,
        "missing_confidence": 0,
        "missing_candles": 0,
        "unsupported_direction": 0,
    }

    for t in trades:
        if not isinstance(t, dict):
            continue

        window_slug = t.get("window_slug")
        if not window_slug:
            skipped["missing_window_slug"] += 1
            continue

        start_ts = _parse_window_start_ts(str(window_slug))
        if start_ts is None:
            skipped["bad_window_slug"] += 1
            continue

        direction = (t.get("direction") or "").strip().upper()
        if not direction:
            skipped["missing_direction"] += 1
            continue
        if direction not in {"UP", "DOWN"}:
            skipped["unsupported_direction"] += 1
            continue

        confidence = _safe_float(t.get("confidence"))
        if confidence is None or not math.isfinite(confidence):
            skipped["missing_confidence"] += 1
            continue

        realized = _realized_up(close_by_ts, start_ts=start_ts, granularity=int(args.granularity))
        if realized is None:
            skipped["missing_candles"] += 1
            continue

        p_up = _p_up_from_trade(direction=direction, confidence=float(confidence))
        if p_up is None:
            skipped["missing_confidence"] += 1
            continue

        y = 1.0 if realized else 0.0
        brier = (float(p_up) - y) ** 2

        correct = bool((direction == "UP" and realized) or (direction == "DOWN" and not realized))

        price = _safe_float(t.get("price"))
        usdc = _safe_float(t.get("usdc"))

        edge_vs_price = None
        if price is not None and math.isfinite(price):
            # price is implied probability for the chosen direction token
            edge_vs_price = float(confidence) - float(price)

        rows.append(
            Row(
                window_slug=str(window_slug),
                start_ts=int(start_ts),
                direction=direction,
                confidence=float(confidence),
                price=price,
                usdc=usdc,
                realized_up=bool(realized),
                correct=correct,
                p_up=float(p_up),
                brier=float(brier),
                edge_vs_price=edge_vs_price,
            )
        )

    n = len(rows)
    if n == 0:
        print("No evaluatable trades found.")
        print("Skipped counts:", skipped)
        return 2

    accuracy = sum(1 for r in rows if r.correct) / n
    brier_mean = statistics.mean(r.brier for r in rows)

    edges = [r.edge_vs_price for r in rows if r.edge_vs_price is not None and math.isfinite(r.edge_vs_price)]

    # Calibration buckets on confidence vs observed correctness
    bucket = float(args.bucket)
    calib: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        lbl = _bucket_label(r.confidence, bucket)
        b = calib.setdefault(lbl, {"n": 0, "wins": 0, "avg_conf": 0.0, "avg_edge": 0.0, "edge_n": 0})
        b["n"] += 1
        b["wins"] += 1 if r.correct else 0
        b["avg_conf"] += r.confidence
        if r.edge_vs_price is not None and math.isfinite(r.edge_vs_price):
            b["avg_edge"] += r.edge_vs_price
            b["edge_n"] += 1

    # finalize averages
    for lbl, b in calib.items():
        b["win_rate"] = (b["wins"] / b["n"]) if b["n"] else None
        b["avg_conf"] = (b["avg_conf"] / b["n"]) if b["n"] else None
        b["avg_edge"] = (b["avg_edge"] / b["edge_n"]) if b.get("edge_n") else None

    report = {
        "trades_file": str(trades_path),
        "candles_file": str(candles_path),
        "granularity": int(args.granularity),
        "n_trades": n,
        "accuracy": accuracy,
        "brier": brier_mean,
        "edge": {
            "n": len(edges),
            "mean": statistics.mean(edges) if edges else None,
            "median": statistics.median(edges) if edges else None,
            "min": min(edges) if edges else None,
            "max": max(edges) if edges else None,
        },
        "calibration": dict(sorted(calib.items(), key=lambda kv: kv[0])),
        "skipped": skipped,
    }

    print("=== Trade-vs-BTC sanity report ===")
    print(f"Trades evaluated: {n}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Brier: {brier_mean:.4f} (lower is better)")
    if edges:
        print(
            "Edge vs price (confidence - price): "
            f"mean={report['edge']['mean']:.4f} median={report['edge']['median']:.4f} "
            f"min={report['edge']['min']:.4f} max={report['edge']['max']:.4f}"
        )
    else:
        print("Edge vs price: (no price fields found)")

    print("\nCalibration (by confidence bucket):")
    for lbl, b in report["calibration"].items():
        avg_edge = b.get("avg_edge")
        avg_edge_s = f"{avg_edge:.4f}" if isinstance(avg_edge, (int, float)) else "-"
        print(
            f"  {lbl}: n={b['n']:3d} win_rate={b['win_rate']:.3f} "
            f"avg_conf={b['avg_conf']:.3f} avg_edge={avg_edge_s}"
        )

    if args.out_csv:
        out_csv = Path(args.out_csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "window_slug",
                    "start_ts",
                    "direction",
                    "confidence",
                    "price",
                    "usdc",
                    "realized_up",
                    "correct",
                    "p_up",
                    "brier",
                    "edge_vs_price",
                ]
            )
            for r in rows:
                w.writerow(
                    [
                        r.window_slug,
                        r.start_ts,
                        r.direction,
                        r.confidence,
                        r.price,
                        r.usdc,
                        int(r.realized_up),
                        int(r.correct),
                        r.p_up,
                        r.brier,
                        r.edge_vs_price,
                    ]
                )
        print(f"\nWrote rows CSV: {out_csv}")

    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"Wrote report JSON: {out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
