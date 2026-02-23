# Discord / Whop Post — v0.4.8

**Copy-paste the text below into your Whop or Discord announcement channel.**

---

🚀 **Crypto5min PolyTrader v0.4.8 — Fill Rate Fix**

Big one here — this update fixes the #1 reason trades weren't executing.

**What was happening:**
The bot was placing limit orders at the model's predicted price, but on these fast 5-minute markets, nobody was selling at that exact price. Result: **~70–80% of orders went unfilled.** The bot was making correct predictions but not actually getting into the trade.

**What's fixed:**

✅ **Fill-or-Kill (FOK) market orders for ALL trades** — Every trade now fills instantly at the best available price, or is canceled on the spot. No more orders sitting on the book waiting for a match that never comes. Fill rate goes from ~20% → ~100%.

✅ **Ghost trade prevention** — If a FOK order can't fill (empty book), it's now correctly recorded as "canceled" instead of appearing as a stuck "posted" order. This prevents the same ghost-trade buildup that v0.4.6 fixed.

✅ **Same safety controls** — Edge gate, Kelly sizing, risk rails, bet caps — all unchanged. The bot still only trades when it detects an edge. The price you pay is capped (you won't overpay on thin books).

**What does this mean for you?**
- Way more of your trades will actually execute — virtually all of them
- Fewer "W unfilled" / "L unfilled" entries cluttering your trade history
- The bot's predictions are the same — it's just actually getting into the trades now

**How to update:**

If you're on a VPS (recommended), the update is already live — just restart:
```
docker compose down && docker compose up -d --build
```

If you're running locally with Docker Desktop:
1. Download the new zip from Whop
2. Extract it next to your old folder
3. Run `update.ps1` (Windows) or `update.sh` (Mac/Linux) — it copies your settings + trade history automatically
4. Start with `docker compose up -d --build`

Your settings, trade history, and balance are all preserved during updates.

Full changelog: see `CHANGELOG_v0.4.8.md` in the zip.

Questions? Drop them here or DM me 👊

---

*End of post*
