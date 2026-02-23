# Whop + social copy (professional / compliant)

> Use this as a starting point. Avoid profit promises. Keep it factual.

## 1) Whop listing headline options

- **Crypto5min PolyTrader — 5‑minute BTC direction bot (with safety rails + ops visibility)**
- **Trade BTC every 5 minutes — dashboard + auto-ops (redeem, logs, risk caps)**
- **Crypto5min PolyTrader — signals, risk controls, and a noob-friendly dashboard**

## 2) Short description (above-the-fold)

Crypto5min PolyTrader generates **UP/DOWN** direction signals for BTC on a rolling **5‑minute window**, with built-in safety rails:

- Confidence gating (trade only when the model is confident)
- Risk caps + cooldowns (prevents runaway sizing)
- Ops visibility (structured events + terminal-style logs)
- Optional Polymarket mode (advanced): live/dry-run support
- Auto-claim winnings (direct wallet only / EOA-only)
- Optional Arb-first mode (high-confidence): buy UP + DOWN only when the orderbook makes the bundle cheap enough
- Optional Fractional Kelly sizing (1/4 Kelly default)

**Not financial advice. Trading involves risk.**

## 3) “What you get” bullets

- Clean web dashboard (HTMX live updates)
- Paper mode for safe onboarding
- Dry-run mode for Polymarket workflows
- Live mode (advanced) for real execution
- Ops Events tab + Terminal tab for transparency
- Setup wizard that writes a local `config/.env`
- Docker-based deploy workflow (VPS friendly)

## 4) Compliance / risk disclosure snippet

This is a software tool that generates signals and can automate actions when enabled. It does not guarantee results. Crypto markets are volatile; you can lose money.

## 5) Launch post (Whop / Discord / X)

🚀 **New release: Crypto5min PolyTrader**

It’s a 5‑minute BTC direction bot with a dashboard that’s actually usable:

- Confidence gating + risk rails
- Ops Events + Terminal logs (see what it’s doing)
- Polymarket mode (advanced) with auto‑redeem winners (EOA‑only)

If you’re new: start in **paper mode**, watch it for a day, then move to dry‑run.

**Not financial advice.**

## 6) FAQ snippets

**Q: Why do some wins show “redeeming” instead of “redeemed”?**
A: “Redeeming” means the on-chain redeem transaction is submitted and pending confirmation. “Redeemed” appears after the receipt is confirmed.

**Q: Does it work with Safe / multisig / proxy wallets?**
A: On-chain redeem/withdraw is EOA-only by design.

**Q: Can it top up gas automatically?**
A: Optional. It can preview/execute a USDC→gas swap via 0x Swap API if configured, but still requires some existing gas to send transactions.

**Wallet requirement:**
Works with standard wallets like MetaMask/Rabby where you control the private key/seed phrase. It does not support Safe/multisig/smart wallets for auto‑redeem/withdraw.
