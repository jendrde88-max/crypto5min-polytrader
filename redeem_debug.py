#!/usr/bin/env python3
import json

trades = json.load(open('logs/poly_trades_remote.json'))

# Check if the unredeemed position slugs exist in trade log
for slug in ['btc-updown-5m-1771175400', 'btc-updown-5m-1771176000', 'btc-updown-5m-1771288200']:
    matches = [t for t in trades if t.get('window_slug') == slug]
    if matches:
        for t in matches:
            resp = t.get('response', {})
            taking = resp.get('takingAmount', 0) if isinstance(resp, dict) else 0
            resp_status = resp.get('status', '') if isinstance(resp, dict) else ''
            print(f"FOUND {slug}:")
            print(f"  resolved={t.get('resolved')} order_status={t.get('order_status')} redeem_status={t.get('redeem_status', 'NONE')}")
            print(f"  filled_size={t.get('filled_size')} condition_id={t.get('condition_id', '')[:20]}...")
            print(f"  resp.status={resp_status} taking={taking}")
            print(f"  redeem_attempted_ts={t.get('redeem_attempted_ts', 'NONE')}")
            print(f"  redeem_tx_hash={t.get('redeem_tx_hash', 'NONE')}")
    else:
        print(f"NOT FOUND: {slug}")
    print()

# Now simulate the candidate selection function
print("=== Simulating select_redeem_candidates ===")
import time
now = int(time.time())
retry_sec = 10 * 60  # default 10 min

candidates = []
for idx, t in enumerate(trades):
    if t.get('resolved') != 'win':
        continue
    order_status = str(t.get('order_status') or '').strip().lower()
    if order_status in ('canceled', 'canceled_market_resolved', 'expired'):
        continue
    resp = t.get('response') or {}
    taking = 0.0
    if isinstance(resp, dict):
        try:
            taking = float(resp.get('takingAmount') or 0)
        except:
            pass
    filled = float(t.get('filled_size') or 0) if t.get('filled_size') else 0.0
    if order_status not in ('filled', 'matched', 'posted', 'open', 'partial', 'unknown', '') and filled <= 0 and taking <= 0:
        continue
    if t.get('redeem_status') == 'success':
        continue
    if t.get('redeem_status') == 'dropped':
        slug = str(t.get('window_slug') or '').strip()
        candidates.append(slug)
        continue
    last_attempt = int(float(t.get('redeem_attempted_ts') or 0))
    last_submit = int(float(t.get('redeem_submitted_ts') or 0))
    last = max(last_attempt, last_submit)
    if last and (now - last) < retry_sec:
        print(f"  SKIPPED (retry wait): {t.get('window_slug')} last_attempt={last} age={now-last}s")
        continue
    slug = str(t.get('window_slug') or '').strip()
    candidates.append(slug)

print(f"Candidates ({len(candidates)}):")
for c in candidates:
    print(f"  {c}")

# Check for orphan detection - what condition IDs are known?
known_cids = set()
for t in trades:
    cid = str(t.get('condition_id') or t.get('conditionId') or '').strip()
    if cid:
        known_cids.add(cid)
print(f"\nKnown condition IDs in trade log: {len(known_cids)}")

# The 2 non-BTC positions (Dortmund, Sampdoria) - would they be found as orphans?
# Their condition IDs won't be in known_cids since they're not bot trades
print("\nOrphan redeem should catch Dortmund/Sampdoria since they're not in trade log")
print("But only if fetch_positions returns them AND they have currentValue > 0.01")
