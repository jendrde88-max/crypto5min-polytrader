# Discord / Whop Post — v0.4.7

**Copy-paste the text below into your Whop or Discord announcement channel.**

---

🚀 **Crypto5min PolyTrader v0.4.7 — Reliability Update**

Hey everyone — this update fixes the #1 issue that could cause the bot to stop trading and sit at $0:

**What was happening:**
Old "ghost" trades from resolved markets were clogging the resolution queue. The bot would check those first, hit its limit, and never get to your real pending trades — so winnings weren't redeemed and the balance stayed at $0.

**What's fixed:**

✅ **Resolution loop fix** — The bot now checks your newest trades first instead of oldest-first, and skips stale ghost trades entirely. Winning trades get resolved and redeemed immediately.

✅ **Orphan redeem dedup** — If a redeem tx gets stuck or dropped, the bot won't keep re-submitting it (saves gas).

✅ **Balance warning** — Logs now clearly show when a trade is skipped due to low balance (instead of silently doing nothing).

✅ **Redeem counter fix** — The dashboard now counts ALL successful redeems, not just trade-based ones.

✅ **Snipe pricing fix** — Snipe trades use fresh price data instead of potentially stale values.

**How to update:**

If you're running on a VPS (recommended), the update was already pushed — just restart your container:
```
docker compose down && docker compose up -d --build
```

If you're running locally with Docker Desktop:
1. Download the new zip from Whop
2. Extract it next to your old folder
3. Run `update.ps1` (Windows) or `update.sh` (Mac/Linux) — it copies your `.env` and trade history automatically
4. Start with `docker compose up -d --build`

Your settings, trade history, and balance are all preserved during updates.

Full changelog: see `CHANGELOG_v0.4.7.md` in the zip.

Questions? Drop them here or check `SUPPORT.md` in the zip.

---

*End of post*
