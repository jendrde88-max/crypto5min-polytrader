"""Check settlement status of today's positions."""
import json
import time
import requests

addr = "0xf8764f91A3b8f6bF111e9EC5c670B541415D8975"
url = f"https://data-api.polymarket.com/positions?user={addr}&limit=200&sizeThreshold=0.01"
r = requests.get(url, timeout=15)
positions = r.json()

now = time.time()
# Find positions with non-zero price (active/winning)
active = [p for p in positions if float(p.get("curPrice", 0)) > 0]
print(f"Positions with non-zero price: {len(active)}")
for p in active:
    title = p.get("title", "?")[:70]
    outcome = p.get("outcome", "?")
    size = float(p.get("size", 0))
    cur_price = float(p.get("curPrice", 0))
    value = size * cur_price
    resolved = p.get("resolved", False)
    cond_id = p.get("conditionId", "?")[:16]
    asset = p.get("asset", "?")[:16]
    print(f"  [{outcome}] {title}")
    print(f"    cond={cond_id}  size={size:.2f}  price={cur_price:.4f}  value=${value:.2f}  resolved={resolved}")
    print()

# Also check the CLOB settlement endpoint
print("--- Checking CLOB for market resolution ---")
for p in active:
    cond_id = p.get("conditionId", "")
    if not cond_id:
        continue
    try:
        url2 = f"https://clob.polymarket.com/markets/{cond_id}"
        r2 = requests.get(url2, timeout=10)
        if r2.ok:
            mkt = r2.json()
            end_date = mkt.get("end_date_iso", "?")
            active_flag = mkt.get("active", "?")
            closed = mkt.get("closed", "?")
            resolved_flag = mkt.get("resolved", "?")  
            title = p.get("title", "?")[:50]
            print(f"  {title}: active={active_flag} closed={closed} resolved={resolved_flag} end={end_date}")
    except Exception as e:
        print(f"  ERROR checking {cond_id[:16]}: {e}")
