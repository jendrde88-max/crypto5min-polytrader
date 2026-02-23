# Discord Announcement — Crypto5min PolyTrader v0.6.6

Copy everything below the line into Discord:

---

# 🔧 Crypto5min PolyTrader — v0.6.6 Hotfix

Quick but important patch dropping now. **If your dashboard settings weren't sticking, this is the fix.**

## What's fixed

### 🚨 Delta First & Delta Pricing toggles now save correctly

These two dashboard toggles were **silently reverting** every time you hit Save Settings. They looked like they changed, but the backend never actually saved the new value.

**Why this matters:** With Delta First stuck ON and Snipe turned OFF, the bot had **zero entry paths** — it literally couldn't place any trades. If you turned off snipe expecting ML trades to take over and nothing happened, this was the bug.

Both toggles now save and persist correctly.

### ✅ Full settings audit

We audited every single toggle across all settings panels:
- **10 toggles** in Polymarket Settings — all working
- **2 toggles** in Model Settings — all working
- **1 toggle** in Gas Settings — working

**All 13 dashboard toggles verified. No other broken settings found.**

---

## How to update

Your dashboard should show a blue **"Update available"** banner. Click **Install Update** — done. Bot restarts automatically.

If you don't see the banner, try refreshing your dashboard page.

### Manual update (Docker)
```
docker compose down
# Replace files
docker compose up -d --build
```

---

*Questions? Drop them in the help channel.*
