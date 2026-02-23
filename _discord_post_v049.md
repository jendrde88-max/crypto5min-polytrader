# Discord / Whop Post — v0.4.9

**Copy-paste the text below into your Whop or Discord announcement channel.**

---

🔧 **Crypto5min PolyTrader v0.4.9 — FOK Hotfix**

Quick but important fix — read on.

**What happened:**
v0.4.8 added Fill-or-Kill (FOK) orders so your trades fill instantly. Great idea, but we found that **every FOK order was silently failing** because Polymarket's API requires amounts to be rounded to 2 decimal places. The bot was sending amounts like `$69.57142857` instead of `$69.57` — so the API rejected every FOK order.

Your trades were still going through because the bot has a GTC fallback that caught every failure. **No trades were lost.** But the whole point of FOK (faster, instant fills) wasn't actually working.

**What's fixed:**

✅ **FOK orders actually work now** — amounts are properly rounded before submission. Your trades now fill via the fast FOK path instead of always falling through to the slower GTC backup.

**Do I need to do anything?**

Nope. No settings changes needed. If you're on a VPS, the update is already live — just restart:

```
docker compose down && docker compose up -d --build
```

If you're running locally, grab the new zip from Whop and run the update script.

Full changelog: see `CHANGELOG_v0.4.9.md` in the zip.

Questions? Drop them here or DM me 👊

---

*End of post*
