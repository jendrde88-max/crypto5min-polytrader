# Discord / Whop Post — v0.4.12

**Copy-paste the text below into your Whop or Discord announcement channel.**

---

🐛 **Crypto5min PolyTrader v0.4.12 — Trades Working Again**

Quick hotfix. If your dashboard was showing trades as "unfilled" even after v0.4.11, this is why — and it's now fixed.

**What was wrong:**

A missing file in the new arb module was crashing the bot's trade loop every 5 minutes. The bot was still running, still making predictions, still showing on the dashboard — but it **couldn't actually place any orders**. This affected everyone with arb-first mode enabled (which is the default).

**What's fixed:**

✅ **Trade loop no longer crashes** — missing package file added, arb module loads correctly
✅ **Normal trades work again** — the crash was blocking ALL trades, not just arb
✅ **Arb-first mode works** — complement arbitrage (buy both sides when combined price < $1) is now functional

**Do I need to do anything?**

Your bot will auto-update if auto-updates are enabled. Otherwise:

**VPS:**
```
docker compose down && docker compose up -d --build
```

**Local:** Grab the new zip from Whop and run the update script.

No settings changes needed. Everything just works with your existing config.

Questions? Drop them here 👊

---

*End of post*
