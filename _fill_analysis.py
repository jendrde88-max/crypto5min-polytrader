import json, time

trades = json.load(open("/app/logs/poly_trades.json"))
now = time.time()

# Split by order_type
fok = [t for t in trades if t.get("order_type") == "FOK"]
gtc = [t for t in trades if not t.get("order_type")]

fok_filled = [t for t in fok if t.get("order_status") == "filled"]
gtc_filled = [t for t in gtc if t.get("order_status") == "filled"]

print(f"=== FILL RATE BY ORDER TYPE ===")
print(f"FOK (snipe): {len(fok_filled)}/{len(fok)} filled ({100*len(fok_filled)/max(1,len(fok)):.0f}%)")
print(f"GTC (normal): {len(gtc_filled)}/{len(gtc)} filled ({100*len(gtc_filled)/max(1,len(gtc)):.0f}%)")

# Last 20 trades breakdown
last20 = trades[-20:]
fok20 = [t for t in last20 if t.get("order_type") == "FOK"]
gtc20 = [t for t in last20 if not t.get("order_type")]
fok20f = [t for t in fok20 if t.get("order_status") == "filled"]
gtc20f = [t for t in gtc20 if t.get("order_status") == "filled"]
print(f"\nLast 20 trades:")
print(f"  FOK: {len(fok20f)}/{len(fok20)} filled")
print(f"  GTC: {len(gtc20f)}/{len(gtc20)} filled")

# Win_unfilled counts
wuf_all = [t for t in trades if t.get("resolved") == "win_unfilled"]
wuf_recent = [t for t in trades[-50:] if t.get("resolved") == "win_unfilled"]
print(f"\nWin_unfilled: {len(wuf_all)} total, {len(wuf_recent)} in last 50")

# Resolution breakdown last 50
res = {}
for t in trades[-50:]:
    r = t.get("resolved") or "unresolved"
    res[r] = res.get(r, 0) + 1
print(f"\nLast 50 resolutions: {res}")

# Check last 10 detail
print(f"\n=== LAST 10 TRADES DETAIL ===")
for t in trades[-10:]:
    age = int(now - t.get("placed_ts", 0))
    ot = t.get("order_type") or "GTC"
    st = t.get("order_status", "?")
    res = t.get("resolved") or "-"
    fs = t.get("filled_size", 0)
    px = t.get("price", 0)
    d = t.get("direction", "?")
    slug = t.get("window_slug", "?")[-20:]
    fa = t.get("fill_attempts", 0)
    print(f"  {ot:3s} {d:4s} px={px:.2f} st={st:30s} filled=${fs:<8.2f} res={res:15s} attempts={fa} {slug} ({age//60}m)")
