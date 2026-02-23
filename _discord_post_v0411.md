# Discord / Whop Post — v0.4.11

**Copy-paste the text below into your Whop or Discord announcement channel.**

---

🔧 **Crypto5min PolyTrader v0.4.11 — FOK Actually Works Now**

Remember the v0.4.9 fix that was supposed to make FOK orders work? Turns out it only fixed half the problem. Here's what happened and what's actually fixed now.

**What was still broken:**
Even after v0.4.9 rounded the order amounts, the Polymarket client library **re-calculates** the number of shares internally (amount ÷ price). BTC 5-minute markets use a tick size (`0.001`) that produces share amounts with **5 decimal places** — but the API only allows **4**. Every FOK order was still getting rejected, silently falling back to GTC, and the GTC order wasn't filling before the market resolved.

That's why you were seeing **"W unfilled"** — the bot predicted correctly, but never actually got into a position.

**What's fixed:**

✅ **FOK orders now force the correct rounding** — we override the tick size at the library level so share amounts stay within the API's 4-decimal limit. This fixes the actual root cause, not just the symptoms.

**What does this mean?**

- Your winning predictions now actually result in **filled positions and payouts**
- Trades fill in a single API call — no more slow GTC fallback
- No more "W unfilled" showing up on your trade history

**Do I need to do anything?**

Nope. No settings changes needed. If you're on a VPS, just restart:

```
docker compose down && docker compose up -d --build
```

If you're running locally, grab the new zip from Whop and run the update script.

Full changelog: see `CHANGELOG_v0.4.11.md` in the zip.

Questions? Drop them here or DM me 👊

---

*End of post*
