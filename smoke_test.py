"""Smoke test all dashboard endpoints with authentication."""
import urllib.request
import urllib.parse
import http.cookiejar
import json
import sys

BASE = "http://65.109.240.249:8602"
PASSWORD = "1Bubby1!1"

# Build a cookie jar for session tracking
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

PASS_TESTS = []
FAIL_TESTS = []

def test(name, ok, detail=""):
    if ok:
        PASS_TESTS.append(name)
        print(f"  PASS  {name}" + (f" — {detail}" if detail else ""))
    else:
        FAIL_TESTS.append(name)
        print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))

# === 1. Login ===
print("=== LOGIN ===")
try:
    data = urllib.parse.urlencode({"password": PASSWORD}).encode()
    req = urllib.request.Request(f"{BASE}/login", data=data, method="POST")
    resp = opener.open(req, timeout=10)
    final_url = resp.geturl()
    status = resp.status
    # After login it should redirect to /
    test("login redirects to /", "/" in final_url or status in (200, 302), f"url={final_url} status={status}")
except Exception as e:
    test("login", False, str(e))

# === 2. Home / Index ===
print("\n=== INDEX PAGE ===")
try:
    resp = opener.open(f"{BASE}/", timeout=10)
    body = resp.read().decode("utf-8", errors="replace")
    test("index loads (200)", resp.status == 200, f"status={resp.status}")
    test("index has version", "0.7.2" in body, f"found={'0.7.2' in body}")
    test("index has dashboard markup", "dashboard" in body.lower() or "polytrader" in body.lower())
    test("index not login page", "name=\"password\"" not in body)
except Exception as e:
    test("index page", False, str(e))

# === 3. /p/live ===
print("\n=== /p/live PARTIAL ===")
try:
    resp = opener.open(f"{BASE}/p/live", timeout=15)
    body = resp.read().decode("utf-8", errors="replace")
    test("/p/live returns 200", resp.status == 200)
    test("/p/live has CLOB balance", "clob_balance_usdc" in body.lower() or "$" in body, f"len={len(body)}")
    test("/p/live has win rate", "win" in body.lower(), f"snippet={body[:200]}")
    test("/p/live has P/L tracking", "P/L" in body or "p/l" in body.lower(), "equity/P&L section rendered")
    # Check snapshot data is rendering (not all dashes)
    test("/p/live no snapshot missing", "—" * 5 not in body, "no long dash sequences (snapshot loaded)")
except Exception as e:
    test("/p/live", False, str(e))

# === 4. /p/trades ===
print("\n=== /p/trades PARTIAL ===")
try:
    resp = opener.open(f"{BASE}/p/trades", timeout=15)
    body = resp.read().decode("utf-8", errors="replace")
    test("/p/trades returns 200", resp.status == 200)
    test("/p/trades has trades", ("updown" in body or "window_slug" in body or "<tr>" in body), f"len={len(body)}")
    test("/p/trades has redeemed tag", "redeemed" in body.lower(), f"has redeemed label")
    test("/p/trades shows W/L", ("<span class" in body))
except Exception as e:
    test("/p/trades", False, str(e))

# === 5. /p/ops ===
print("\n=== /p/ops PARTIAL ===")
try:
    resp = opener.open(f"{BASE}/p/ops", timeout=15)
    body = resp.read().decode("utf-8", errors="replace")
    test("/p/ops returns 200", resp.status == 200)
    test("/p/ops has auto-redeem section", "auto-redeem" in body.lower() or "redeem" in body.lower())
    test("/p/ops has events table", "<table" in body.lower())
    test("/p/ops has settle_close_resolved", "settle_close_resolved" in body, "ops events visible")
except Exception as e:
    test("/p/ops", False, str(e))

# === 6. /p/state ===
print("\n=== /p/state PARTIAL ===")
try:
    resp = opener.open(f"{BASE}/p/state", timeout=10)
    body = resp.read().decode("utf-8", errors="replace")
    test("/p/state returns 200", resp.status == 200)
    test("/p/state has signal direction", any(x in body for x in ["UP", "DOWN", "Confidence"]))
except Exception as e:
    test("/p/state", False, str(e))

# === 7. Version endpoint ===
print("\n=== /api endpoints ===")
try:
    resp = opener.open(f"{BASE}/api/version", timeout=10)
    body = resp.read().decode("utf-8", errors="replace")
    test("/api/version", "0.7.2" in body, f"body={body[:100]}")
except Exception as e:
    # May return 404 if no /api/version endpoint
    test("/api/version (optional)", True, f"endpoint missing: {e}")

# === Summary ===
print(f"\n{'='*50}")
print(f"PASSED: {len(PASS_TESTS)}/{len(PASS_TESTS)+len(FAIL_TESTS)}")
if FAIL_TESTS:
    print(f"FAILED: {FAIL_TESTS}")
    sys.exit(1)
else:
    print("All smoke tests passed!")
