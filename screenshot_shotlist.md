# Screenshot shotlist (no secrets)

Goal: show the product looks real, is operational, and has safety rails **without exposing** wallet addresses, balances, API keys, or server IPs.

## Before you screenshot

- Use **paper** or **dry-run** mode unless you intentionally want “live”.
- Make sure the UI shows **no private keys** (never screenshot the Setup page while the key field is filled).
- Consider setting a temporary dashboard password and using a fresh browser profile.
- Recommended viewport: **1440×900** (clean Whop-friendly crops).

## Shot 1 — Hero dashboard (Signals + Controls)

- Tab: **Signal & Trading**
- Capture: sidebar + signal card + the big direction arrow + confidence + “updated X ago”.
- Make sure the timestamp shows in **Local** time (after our recent change).

## Shot 2 — Recent Trades showing redeem status

- Tab: **Trades & Equity**
- Capture the table with at least 1 row showing:
  - `W` + `redeemed` badge
  - `W` + `redeeming` badge
  - and a few pending `…`

Tip: crop to show the **Result** column clearly.

## Shot 3 — Ops Events (proof it’s doing work)

- Tab: **Ops Events**
- Capture the recent event list that includes:
  - `redeem_positions`
  - `redeem_reconcile`
  - any trade placement events

## Shot 4 — Terminal tab (raw log visibility)

- Tab: **Terminal**
- Capture the last lines showing periodic requests / background loops.

## Shot 5 — Wallet care / Gas status

- Tab: **Signal & Trading**
- Capture the gas balance display + any low-gas badge (if safe to show).

If you don’t want to expose balances, crop so it’s clear *what* it is without showing exact numbers.

## Shot 6 — Setup Wizard (blank fields only)

- Page: **/setup**
- Capture the wizard showing what it asks for, **with all secret fields empty**.

## Optional shots

- Equity chart (clean crop)
- Controls panel showing confidence threshold + bet size rails
- Withdraw section (disabled by default) with warning text
