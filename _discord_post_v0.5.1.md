# Discord Announcement — v0.5.1 "Delta-First"

---

## 🚀 v0.5.1 — Strategy Overhaul: "Delta-First"

After analysing live trade data, I found the ML model was outputting near-constant predictions — resulting in a **27% win rate** (worse than a coin flip). The root cause: the CNN-LSTM model doesn't have enough signal on 5-minute data, and entering at T-30s means trading on stale information while paying market prices ($0.82–$0.99 per share).

### What changed

**Before (≤ v0.4.x):**
- ML model predicts direction at T-30s → places trade at whatever the market is asking
- 27% observed win rate — model was essentially guessing
- Entry prices $0.82–$0.99 per share (need 82–99% accuracy to break even)

**After (v0.5.1):**
- **Delta-first mode** — ML trades are DISABLED by default
- **Snipe at T-10s** using live Chainlink delta is now the **sole entry mechanism**
- **Delta-based price gate** — the bot checks the live ask against a delta-derived tier:
  - Small delta → strict gate ($0.52) → only trades if the market is cheap (high ROI)
  - Large delta → permissive gate ($0.97) → fills at almost any market price
- If the ask exceeds the gate → trade is skipped (signal isn't worth the price)
- If the ask passes → FOK fills at standard pricing (best available ask + buffer)

### Why this works

This approach was validated by Archetapp, the most profitable documented open-source Polymarket bot ($313 → $414k on BTC 5-min markets). Their key insight:

> *"Window delta is king. Never skip a trade. Entry at T-10s is the sweet spot. Delta-based pricing prevents overpaying."*

At T-10s before window close, 4 minutes 50 seconds of price movement have already happened. If BTC has moved >0.02% from the window open (measured by the same Chainlink oracle that resolves the market), the remaining 10 seconds are unlikely to reverse the direction.

### New settings

| Variable | Default | What it does |
|---|---|---|
| `C5_DELTA_FIRST` | `true` | Disable ML trades, snipe-only mode |
| `C5_DELTA_PRICING` | `true` | Delta-based price gate (skip if ask > tier) |
| `C5_DELTA_PRICE_T1` – `T5` | `$0.52–$0.97` | Tunable pricing gate tiers |

### Dashboard

Two new toggles in the sidebar under **Trading**:
- **Delta-first mode** — on/off (default ON)
- **Delta pricing** — on/off (default ON)

Plus updated **How It Works** legend explaining both features.

### Backward compatibility

Set `C5_DELTA_FIRST=false` (or toggle off in dashboard) to bring back the ML+snipe hybrid. The ML model still trains and shows predictions on the dashboard — it just doesn't trigger trades by default.

### How to update

Your bot will auto-update on next restart, or run:
```
./update.sh
```

---

**TL;DR:** Stopped guessing. Now the bot only trades when real-time data (Chainlink delta) confirms the direction, and only when the market price is worth it for the signal strength. Fewer trades, but much smarter ones.
