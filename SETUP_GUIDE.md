# Setup Guide — Crypto5min PolyTrader

> **New to all of this?** Don't worry. This guide walks you through every step, assumes zero crypto experience, and explains everything along the way. If you get stuck, check the [FAQ & Troubleshooting](#faq--troubleshooting) section at the bottom.

---

## ⚡ Quick Start (5 steps, ~5 minutes)

| Step | What to do |
|------|------------|
| **1** | **Choose how to run it** — [Railway](https://railway.com?referralCode=polytrader) (easiest, no server needed), OR get a VPS — [Vultr](https://www.vultr.com/?ref=9869564), [Hetzner](https://hetzner.com), [DigitalOcean](https://digitalocean.com) ($5-10/mo). Or run on Windows with Docker Desktop. |
| **2** | **Download & unzip** — `wget <your-download-link> && unzip Crypto5min_PolyTrader_*.zip && cd crypto5min-polytrader` |
| **3** | **Run the installer** — `bash setup.sh` (auto-installs Docker if missing, builds the bot, starts it) |
| **4** | **Open the Setup Wizard** — Go to `http://YOUR-SERVER-IP:8602` in your browser. Fill in your password, private key, and wallet type. |
| **5** | **Fund your wallet** — Send $10-50 USDC + $1 of POL to the wallet address shown on the dashboard. Done! |

> **That's it.** The bot trains its AI model automatically and starts trading within minutes. Start in **Paper mode** first to verify everything works, then switch to **Live** from the dashboard.

<details>
<summary>📋 Where do I get my private key?</summary>

- **MetaMask users**: Settings → Security → Reveal Private Key
- **Email / Google users**: Go to [reveal.magic.link](https://reveal.magic.link), sign in with the same email you used for Polymarket, and copy the key. The Setup Wizard will also ask for your **Funder Address** (your Polymarket profile wallet address, not your private key).
</details>

---

---

## Deployment Options — Pick Your Path

There are three ways to run Crypto5min PolyTrader. Choose the one that fits you best:

| Option | Best for | Cost | Effort |
|--------|----------|------|--------|
| **A — Railway (cloud, one-click)** | Complete beginners | ~$5/mo | ⭐ Easiest |
| **B — VPS with Docker** | All users, 24/7 reliability | ~$4-6/mo | ⭐⭐ Moderate |
| **C — Windows PC / Windows VPS** | Windows users, no Linux | Free (own PC) or ~$6/mo | ⭐⭐ Moderate |

### Option A — Deploy on Railway (recommended for beginners)

Railway runs your bot in the cloud without you managing any server.

1. Sign up at **[railway.com](https://railway.com?referralCode=polytrader)** (using this link supports the project)
2. Create a new project, select "Empty Project", and drag-and-drop this unzipped folder into the Railway dashboard.
3. Set the required environment variables (Railway will prompt you):
   - `C5_POLY_PRIVATE_KEY` — your wallet private key
   - `C5_POLY_SIGNATURE_TYPE` — `1` for Email/Google, `0` for MetaMask direct
   - `C5_POLY_FUNDER_ADDRESS` — your Polymarket profile address (if Email/Google)
   - `C5_DASHBOARD_PASSWORD` — any password you choose
4. Railway builds and starts the bot automatically
5. Click the generated URL to open your dashboard — done!

> **The `railway.json` file in this zip is pre-configured** — Railway will pick it up automatically.

### Option B — VPS with Docker (recommended for reliability)

A VPS is a small cloud computer that runs 24/7. This is the most reliable option.

**Recommended providers (all confirmed working with Polymarket):**

| Provider | Location | Price | Link |
|----------|----------|-------|------|
| Vultr ⭐ | Amsterdam, Frankfurt, etc. | ~$6/mo | [vultr.com](https://www.vultr.com/?ref=9869564) |
| Hetzner | Helsinki, Finland | ~$4/mo | [hetzner.com/cloud](https://hetzner.com/cloud) |
| DigitalOcean | Amsterdam, Netherlands | ~$6/mo | [digitalocean.com](https://digitalocean.com) |
| Contabo | Bucharest, Romania | ~$4/mo | [contabo.com](https://contabo.com) |

> **Important:** Do NOT use a US-based VPS — Polymarket blocks US IP addresses. Use Europe or Canada.

SSH into your VPS, download the ZIP, run `bash setup.sh`, and follow the Setup Wizard.

### Option C — Windows (PC or Windows VPS)

You can run the bot on a Windows computer or a Windows VPS without any Linux knowledge.

**On your own Windows PC:**
1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) (free)
2. Enable WSL 2 when prompted
3. Extract the bot ZIP, open PowerShell in that folder
4. Run: `docker compose up -d --build`
5. Open `http://localhost:8602` in your browser

**On a Windows VPS (e.g. [Vultr Windows ~$6/mo](https://www.vultr.com/?ref=9869564)):**
1. RDP into your Windows VPS (use Remote Desktop Connection — built into Windows)
2. Inside the VPS, install Docker Desktop (same steps as above)
3. Follow the same Docker steps

> **Note:** For 24/7 trading on your own PC, make sure your computer never sleeps (Power Settings → "Never sleep").

---

## Table of contents

1. [What is Docker and why do I need it?](#1-what-is-docker-and-why-do-i-need-it)
2. [Installing Docker](#2-installing-docker)
3. [Starting the bot](#3-starting-the-bot)
4. [The Setup Wizard](#4-the-setup-wizard)
5. [Dashboard overview](#5-dashboard-overview)
6. [Understanding the modes: Paper → Dry-run → Live](#6-understanding-the-modes-paper--dry-run--live)
7. [Getting your Polymarket private key](#7-getting-your-polymarket-private-key)
    - [7b) Email/Google users: signature type + funder address](#7b-email--google-users-signature-type--funder-address)
8. [Funding your wallet (USDC + gas)](#8-funding-your-wallet-usdc--gas)
9. [Trading strategies explained](#9-trading-strategies-explained)
10. [Bet sizing (Fixed / % / Kelly)](#10-bet-sizing-fixed----kelly)
11. [Settlement, redemption & getting money out](#11-settlement-redemption--getting-money-out)
12. [Updating to a new version](#12-updating-to-a-new-version)
13. [Advanced settings](#13-advanced-settings)
14. [FAQ & Troubleshooting](#14-faq--troubleshooting)

---

## 1) What is Docker and why do I need it?

**Docker** is a free tool that runs apps inside isolated "containers." Think of it like this:

- Without Docker: you'd need to install Python, a bunch of libraries, configure paths, deal with version conflicts...
- With Docker: you run **one command** and everything works. The bot runs inside its own mini-computer.

**You don't need to know how Docker works.** Just install it and let it do its thing.

---

## 2) Installing Docker

### Windows

1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Click **Download for Windows**
3. Run the installer (accept all defaults)
4. **Important:** When asked, enable **WSL 2** (Windows Subsystem for Linux) — check the box
5. Restart your computer when prompted
6. Open **Docker Desktop** from the Start menu
7. Wait for it to fully start — you'll see a **whale icon** in the system tray (bottom-right near the clock)
8. When the whale icon stops animating, Docker is ready

**To verify it works,** open PowerShell and type:
```powershell
docker version
```
You should see version numbers. If you see an error, Docker isn't running yet.

> **Common Windows issue:** If you see "WSL 2 installation is incomplete", open PowerShell **as Administrator** (right-click → Run as Administrator) and run: `wsl --install`, then restart your PC.

### Mac

1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Click **Download for Mac** (choose Apple Silicon or Intel based on your Mac)
3. Open the downloaded `.dmg` file → drag Docker to Applications
4. Open **Docker** from Applications
5. Wait for "Docker Desktop is running" in the menu bar

**To verify:** Open Terminal and type `docker version`.

### Linux (Ubuntu / Debian / most VPS)

Run this single command:
```bash
curl -fsSL https://get.docker.com | sh
```

Then add your user to the Docker group (so you don't need `sudo` every time):
```bash
sudo usermod -aG docker $USER
```
**Log out and log back in** for this to take effect.

**To verify:** Type `docker version` and `docker compose version`.

> **VPS users:** Docker is often pre-installed. Just run `docker version` to check. If it works, skip this step.

---

## 3) Starting the bot

### Step 1: Get the bot files

- Download the ZIP from Whop
- Unzip it into a folder (e.g., `crypto5min-polytrader` on your Desktop, or `/root/crypto5min-polytrader` on a VPS)

### Step 2: Open a terminal in the bot folder

- **Windows:** Open the folder in File Explorer, click the address bar, type `powershell`, press Enter
- **Mac:** Open Terminal, type `cd ` (with a space), then drag the folder into the Terminal window, press Enter
- **Linux/VPS:** `cd /path/to/crypto5min-polytrader`

### Step 3: Run the start command

**Linux / Mac:**
```bash
bash setup.sh
```

**Windows (PowerShell):**
```powershell
docker compose up -d --build
```

> **First time?** This will take **2–5 minutes** to download ~500MB of dependencies. You'll see lots of text scrolling — that's normal. Subsequent starts take ~5 seconds.

### Step 4: Open the dashboard

- **Local:** Open your browser → go to [http://localhost:8602](http://localhost:8602)
- **VPS:** Open your browser → go to `http://YOUR_SERVER_IP:8602`

Replace `YOUR_SERVER_IP` with your actual VPS IP address (e.g., `http://65.109.240.249:8602`).

---

## 4) The Setup Wizard

On first run, the dashboard shows a **Setup Wizard** with two steps:

### Step 1 of 2: Create your password

- Type a password for your dashboard
- This protects the dashboard from random people who find your URL
- **Avoid special characters** like `$`, `"`, `\`, and `#` in your password — these can cause login issues because the `.env` file uses them as control characters. Stick to letters, numbers, and simple symbols like `!`, `@`, `-`, `_`.
- Click **Save and continue**

> **About the setup token:** The wizard URL has a `?token=...` part. This is a one-time security code that prevents random visitors from setting your password. If the token is wrong, just open `/setup` again — it shows the correct token link.

### Step 2 of 2: Polymarket settings (optional)

You can skip this entirely and come back later. If you want to set it up now:

- **Private key:** Your Polymarket wallet private key (see [Section 7](#7-getting-your-polymarket-private-key))
- **Wallet type:** MetaMask/browser wallet, or Email/Google
- **Funder address (only for Email/Google or proxy wallets):** Your Polymarket profile (proxy) address (must be a wallet address like `0x...`, not your private key, and it should be **different** from the wallet address derived from your private key)
- **Max spend per trade (USDC):** How much the bot can spend per 5-minute trade. Start small (e.g. $5).

Click **Save and launch** — the bot starts running!

> **Important:** If you skip wallet setup now, you can add/fix it anytime by going to `/reconfigure` (Setup Wizard Step 2).

---

### 7b) Email / Google users: signature type + funder address

If you log into Polymarket with **email or Google** (not MetaMask), you must use wallet type **Email / Google** and set your Polymarket profile address as funder.

**Very important:**
- `Private key` field = key from `reveal.magic.link`
- `Funder address` field = your **wallet address** from your Polymarket profile (`0x` + 40 hex chars)
- Do **not** paste your private key into the funder field
- Do **not** paste the **same address** as your derived wallet address into the funder field (v0.6.2+ blocks this; proxy/funder must be different)

#### Option A: From the dashboard (easiest — v0.4.14+)

1. Log into your dashboard
2. Go to `/reconfigure` (this re-opens the Setup Wizard)
3. Set **Wallet type** to **Email / Google (MagicLink)**
4. Paste your **Funder Address** (your Polymarket profile address — the one shown on polymarket.com when you click your profile)
5. Click **Save** — changes apply immediately, no restart needed

#### Option B: Manual edit (if you prefer the command line)

```bash
sudo nano config/.env
```

Add these two lines:

```dotenv
C5_POLY_SIGNATURE_TYPE=1
C5_POLY_FUNDER_ADDRESS=0xYOUR_POLYMARKET_PROFILE_ADDRESS
```

- **`C5_POLY_SIGNATURE_TYPE`** — Set to `1` for email/Google users. The default `0` is for MetaMask/browser-wallet users.
- **`C5_POLY_FUNDER_ADDRESS`** — Your Polymarket profile/trading address (the one shown on polymarket.com when you click your profile). This is the address that holds your balance.

Then restart: `docker compose restart`

> **How do I know which type I am?**
> - Log in with **email or Google** → type `1`
> - Connect a **crypto wallet** (MetaMask, Coinbase Wallet, etc.) → type `0` (default, no change needed)
>
> **This is the #1 most common setup issue.** If you see $0 balance but have funds on Polymarket, this is almost certainly the fix.

If you can't edit `config/.env` due to permission errors, use this one-liner instead (replace the values):

```bash
sudo bash -c 'cat >> config/.env << EOF
C5_POLY_SIGNATURE_TYPE=1
C5_POLY_FUNDER_ADDRESS=0xYOUR_POLYMARKET_PROFILE_ADDRESS
EOF'
```

---

## 5) Dashboard overview

The dashboard has several sections:

### Main area (center)

- **Signal:** Shows the current prediction (UP or DOWN) with confidence percentage
- **BTC Price chart:** Live Bitcoin price, updated every 10 seconds
- **Equity curve:** Your paper (simulated) or live trading balance over time
- **Trade log:** Recent trades with outcome (win/loss) and amounts

### Sidebar (left)

- **Mode buttons:** PAPER / DRY-RUN / LIVE — click to switch
- **Status:** Shows if the bot is running, paused, or error
- **Wallet info:** Your wallet address and balances (USDC + gas)
- **Settings:** Click to expand trading settings
- **Paper Balance** (dry-run only): When in dry-run mode, the sidebar shows your virtual USDC balance, realized P&L, win rate, and a "Reset Paper" button. Trades are simulated at the ask price. Set `C5_PAPER_STARTING_CASH` (default $10,000) to change the starting balance.

### "How It Works" tab (top)

This is an **in-dashboard guide** with:
- Getting started steps
- Settings explained (what each toggle does)
- FAQ (frequently asked questions)
- Quick reference table
- Advanced settings

**Read this tab** — it explains everything you see on the dashboard.

---

## 6) Understanding the modes: Paper → Dry-run → Live

Always progress through modes in this order:

| Mode | What happens | Risk |
|------|-------------|------|
| **Paper** | Bot makes predictions, records fake trades. No real money involved. | None |
| **Dry-run** | Bot finds real Polymarket markets, logs what it *would* trade, but doesn't place orders. **Paper PnL** tracks a virtual balance — see fills, P&L, and win rate on the dashboard. | None |
| **Live** | Bot places **real orders** with **real money** on Polymarket. | Real |

**Recommended progression:**

1. **Paper for 1–2 days:** Watch the predictions, check accuracy
2. **Dry-run for a few hours:** Verify it's finding the right markets
3. **Live with $10–20:** Start tiny, verify everything works
4. **Scale up gradually** if you're comfortable

---

## 7) Getting your Polymarket private key

Your Polymarket account has a hidden crypto wallet behind the scenes. To let the bot trade on your behalf, you need its private key.

### How to get it:

1. Log into [polymarket.com](https://polymarket.com) in your browser
2. Go to [reveal.magic.link/polymarket](https://reveal.magic.link/polymarket)
3. It will ask you to verify your identity (email/social login)
4. You'll see a long string starting with `0x...` — that's your private key
5. **Copy it carefully** — do not share it with anyone

### Important safety rules:

- ⚠️ This key controls your entire Polymarket wallet
- 🔒 The bot stores it **only on your server** in `config/.env`
- 💰 **Use a dedicated bot wallet** — never use your main wallet's key
- 🏦 Only put small amounts in the bot wallet ($10–50 to start)
- 🚫 Never paste your key into websites, DMs, or emails

---

## 8) Funding your wallet (USDC + gas)

You need two things in your bot wallet:

### A) USDC (the trading money)

USDC is a stablecoin worth exactly $1. It's what Polymarket uses for all trades.

**How to get USDC into your bot wallet:**

1. **Find your bot wallet address** — it's shown on the dashboard sidebar under "Wallet." It's a long string starting with `0x...`
2. **Buy USDC** on a crypto exchange:
   - [Coinbase](https://coinbase.com) (easiest for US users)
   - [Kraken](https://kraken.com) (easy, worldwide)
   - [Binance](https://binance.com) (worldwide, lowest fees)
3. **Withdraw USDC** to your bot wallet address, selecting **Polygon** as the network

   ⚠️ **CRITICAL:** When withdrawing, you MUST select **Polygon** (sometimes called "Polygon POS") as the network. Do NOT select Ethereum or any other network. **Wrong network = lost funds.**

4. Start with **$10–50** — you can always add more later

### B) Gas (POL / MATIC — the transaction fee token)

Every trade on Polygon costs a tiny fee (fractions of a cent). You pay this fee with a token called **POL** (formerly called MATIC).

**How to get POL/MATIC:**

1. Buy POL or MATIC on the same exchange you used for USDC
2. Withdraw **$1–3 worth** of POL/MATIC to the **same bot wallet address** on **Polygon**
3. That's enough for hundreds of trades

> **If you see a "Low gas" warning** on the dashboard → send more POL/MATIC to your bot wallet.

---

## 9) Trading strategies explained

The bot has three strategies. You can use any combination:

### ML Prediction (disabled in delta-first mode)

A neural network (CNN-LSTM) analyzes 42+ technical indicators from BTC price history and predicts whether the next 5-minute candle will go UP or DOWN.

- **Accuracy:** ~52–55%
- **How it works:** Retrains every hour on fresh data. Makes a prediction at the start of each 5-minute window.
- **When it trades:** Only when confidence exceeds your threshold and Kelly/fixed sizing gives a position.
- **Note (v0.5.0+):** When `C5_DELTA_FIRST=true` (default), ML predictions still run and display on the dashboard, but do **not** trigger trades. The snipe pass is the sole entry mechanism. Set `C5_DELTA_FIRST=false` to re-enable ML trades.

### Snipe mode (on by default — highest accuracy)

A separate strategy that works completely differently from the ML model. **Enabled by default since v0.3.0** because it's the bot's best strategy.

- **How it works:** Waits until the last ~10 seconds before a 5-minute window closes, then checks if BTC has *already* moved up or down from the window open price (using the **Chainlink oracle** — the exact same price feed Polymarket uses to resolve markets). If the move is large enough, trades in that direction.
- **Why it works:** With only 10 seconds left, the direction is mostly locked in. If BTC is already up +0.10%, it's ~85%+ likely to stay UP.
- **Accuracy:** ~80–90%+ when triggered
- **Smart sizing:** Snipe trades automatically bet 2× normal size (configurable via `C5_POLY_SNIPE_BET_MULTIPLIER`). Because accuracy is much higher, it makes sense to bet more on these trades.
- **Trade-off:** Tokens cost more near close ($0.70–0.95 instead of ~$0.50), so profit per trade is smaller
- **Toggle in dashboard:** Sidebar → Trading → Snipe mode → Save (on by default)

### Delta-First mode (v0.5.0+, default ON — recommended)

The bot's default strategy since v0.5.0. **Delta-first makes the snipe pass the ONLY entry mechanism** — ML directional trades are disabled.

- **How it works:** The ML model still trains and displays predictions on the dashboard, but it does NOT trigger trades. Instead, the bot relies exclusively on the T-10s snipe pass using the live Chainlink oracle delta. When the observed BTC move exceeds `C5_SNIPE_MIN_DELTA_PCT` (default 0.02%), a FOK order fires.
- **Why:** Empirical analysis showed the CNN-LSTM model produces near-constant output (degenerate predictions). The Chainlink snipe at T-10s has ~80–90%+ accuracy based on real market data and is validated by the most profitable open-source Polymarket bot strategy.
- **Delta pricing (gate):** When `C5_DELTA_PRICING=true` (default), the bot gates snipe trades based on the live ask vs. the delta magnitude.  If the market asks more than the tier allows for the observed delta, the trade is skipped (too expensive for the signal strength).  If the ask is at or below the tier, the trade executes at standard FOK pricing:
  - Delta < 0.01% → $0.52 gate (ask must be ≤ $0.52 — high ROI, small signal)
  - Delta < 0.02% → $0.58 gate
  - Delta < 0.05% → $0.68 gate
  - Delta < 0.10% → $0.82 gate
  - Delta ≥ 0.10% → $0.97 gate (strong signal, fills at almost any market price)
  - All tier prices are tunable via `C5_DELTA_PRICE_T1` through `C5_DELTA_PRICE_T5` in `.env`
- **To disable:** Set `C5_DELTA_FIRST=false` in `.env` or toggle off in dashboard → Trading → Delta-first. This restores the original ML+snipe hybrid mode.
- **Toggle in dashboard:** Sidebar → Trading → Delta-first mode → Save

### Arb-first mode (optional, risk-free when possible)

Watches the Polymarket orderbook and buys BOTH UP and DOWN shares when the combined cost is briefly below $1.00.

- **How it works:** If UP costs $0.48 and DOWN costs $0.49 = $0.97 total. Since one side MUST pay $1.00, you profit $0.03 per dollar regardless of outcome.
- **Accuracy:** 100% when triggered (guaranteed profit)
- **Trade-off:** Extremely rare. The bot might watch for hours without finding one.
- **Enable in dashboard:** Sidebar → Trading → Arb-first → Save

---

## 10) Bet sizing (Fixed / % / Kelly)

In the dashboard sidebar under **Trading → Bet mode**, you choose how the bot decides how much to trade:

| Mode | How it works | Best for |
|------|-------------|----------|
| **Fixed $** | Every trade uses the same dollar amount (your "Max $/trade" setting) | Beginners. Simple and predictable. |
| **% of balance** | Each trade uses a percentage of your current balance (still capped by max $) | Growing accounts. Trades get bigger as you win. |
| **Kelly** | Math formula that sizes trades based on how confident the model is vs the market price. Multiplied by a safety fraction (default 0.25 = quarter Kelly). | Advanced users. Maximizes long-term growth in theory. |

**Recommendation:** Start with **Fixed $** at a small amount ($2–5). Once you're comfortable, switch to **% of balance** (5–10%) for compound growth. Kelly is for advanced users — it requires the model to be more confident than the live market price before it trades, which means fewer trades overall.

> **Tip:** If you're using Kelly mode and the bot keeps logging `kelly_no_edge`, it means the model's confidence isn't high enough above the live market price. Switch to **percent** mode (5-10%) instead.

---

## 11) Settlement, redemption & getting money out

### How order execution works

When the bot places an order on Polymarket:

1. **Live pricing** — Fetches the real-time best ask from Polymarket's CLOB orderbook (not stale cached data)
2. **Price buffer** — Adds $0.02 above the best ask to cross the spread and ensure a fill
3. **Fill-or-retry** — If the order doesn't fill within 20 seconds, the bot cancels it and re-posts at a higher price (+$0.02), up to 3 attempts
4. **Minimum order size** — Polymarket requires at least 5 shares per order. The bot automatically bumps small orders to meet this minimum.

This means your orders actually fill — no more phantom "wins" sitting unfilled on the orderbook.

**Trading fees:** As of February 2026, most Polymarket markets — including 5-minute crypto markets — have **no trading fees**. Some market types (15-minute crypto, NCAAB, Serie A) do have taker fees (max ~1.56% at a $0.50 share price). The `py_clob_client` library handles fee calculation automatically regardless of whether fees apply. Fee schedules can change — check [docs.polymarket.com](https://docs.polymarket.com/polymarket-learn/trading/fees) for the latest.

### How Polymarket wins work

When a 5-minute window resolves (the outcome is determined):

1. If the bot was **right**, your winning shares are worth $1.00 each
2. The shares need to be **redeemed** (converted back to USDC)
3. The bot can do this automatically if **Auto-redeem** is enabled

### Enable auto-redeem

Auto-redeem is **on by default**. It sends a small on-chain transaction (costs a tiny bit of gas) to claim your winnings.

If you want to verify or change: Dashboard sidebar → Trading → Auto-redeem.

### Getting your money out of the bot

Your funds are always in **your** wallet — the bot can never lock them. To withdraw:

1. **Pause the bot** — click the pause button in the dashboard
2. **Close open positions** — use the Polymarket website or MetaMask
3. **Transfer USDC** — send it from your bot wallet to your personal wallet or exchange
4. **Convert to cash** — sell USDC on your exchange for real dollars

> **Quick method with MetaMask:** Install the MetaMask browser extension, import your bot wallet's private key, and you can manage the wallet directly.

---

## 12) Updating to a new version

### Option A: One-click from the dashboard (recommended)

The dashboard checks for updates automatically and shows a banner when one is available.
You can also check manually:

1. Look at the **bottom-left of the sidebar** — you'll see your **current version** (e.g. v0.4.0)
2. Click the **↻ Check** button next to it
3. If an update is available, a **green banner** appears with release notes
4. Click **"Apply Update"** — the bot downloads, installs, and restarts automatically
5. Refresh the page after ~30 seconds — done!

> **No downtime worry:** The bot saves your settings and trade history automatically. Nothing is lost during updates.

### Option B: Manual update (from ZIP)

When a new version is released:

1. Download the new ZIP from Whop
2. Unzip into a **new folder** (don't overwrite the old one)
3. Open a terminal in the **new** folder
4. Run the update script — it copies your settings and trade history automatically:

**Linux / Mac:**
```bash
bash update.sh /path/to/old/folder
```

**Windows (PowerShell):**
```powershell
.\update.ps1 -OldPath "C:\path\to\old\folder"
```

The script will:
- Copy your `config/.env` (settings & private key)
- Copy your `logs/` folder (trade history & state)
- Copy your `data/` folder (cached candles — saves re-download time)
- Stop the old container
- Build and start the new version

> **Don't want to use the script?** You can still do it manually: copy `config/.env` and `logs/` from the old folder into the new one, then run `docker compose up -d --build`.

> **Your settings and trade history carry over** as long as you copy `config/.env` and `logs/`.

---

## 13) Advanced settings

These are for experienced users. Skip this section if you're just getting started.

### Order safety (live trading)

| Setting | Default | What it does |
| ------- | ------- | ------------ |
| `C5_POLY_AUTO_CANCEL_STALE` | `true` | Auto-cancels orders that don't fill in time |
| `C5_POLY_ORDER_TIMEOUT_SEC` | `120` | Seconds before an unfilled order is considered stale |
| `C5_POLY_COOLDOWN_SECONDS` | `300` | Minimum seconds between trades (prevents overtrading) |
| `C5_POLY_PRICE_BUFFER` | `0.40` | Added above best ask to ensure order fills |
| `C5_POLY_ASK_MODE` | `prefer_live` | How to choose the base ask: `prefer_live` uses live orderbook when available; `legacy_max` uses max(live, Gamma). |
| `C5_POLY_FILL_MAX_ATTEMPTS` | `3` | How many times to retry if order doesn't fill |
| `C5_POLY_FILL_WAIT_SEC` | `20` | Seconds to wait for fill before retrying |
| `C5_POLY_FILL_RETRY_BUMP` | `0.02` | Price increase per retry attempt |
| `C5_POLY_MIN_SHARES` | `5` | Minimum shares per order (Polymarket CLOB minimum) |
| `C5_POLY_REQUIRE_BOOK_DEPTH` | `false` | When enabled, skip trades when there isn't enough cumulative ask-side liquidity to fill your USDC size up to the FOK worst-price cap. Default OFF since v0.6.0 — FOK orders handle thin books safely (they fail instantly with no cost if liquidity is insufficient). |
| `C5_POLY_BOOK_DEPTH_MULT` | `1.10` | Cushion multiplier for the depth check (1.10 = require 10% extra depth to reduce snapshot staleness). |
| `C5_AGGRESSIVE_FILL_MODE` | `true` | Adaptive execution: uses orderbook depth to choose FOK (full size) vs FAK (partial size) instead of skipping on thin books. Also enforces spread/slippage rails below. |
| `C5_MIN_FILL_USDC` | `5.0` | Minimum USDC notional to attempt on thin books. If depth within the price cap is below this (or below the exchange minimum order), the trade is skipped as no-depth. |
| `C5_MAX_SPREAD_BPS` | `200` | If spread is wider than this, the bot will **not** cross as a taker (it will skip taker entries; endgame maker pre-position can still rest without crossing). |
| `C5_MAX_SLIPPAGE_BPS` | `200` | Caps worst-price (price_limit) relative to live best ask to avoid paying far beyond current market. |
| `C5_ENDGAME_SECONDS` | `30` | Endgame window length. From this many seconds remaining down to 10s, the bot can place a small resting maker order (do-not-cross). |
| `C5_ENDGAME_POLL_MS` | `250` | Poll interval inside endgame. Outside endgame the loop stays slower. |
| `C5_MAX_REPRICES` | `2` | Max cancel/replace cycles for endgame maker and final taker retries in the last 10 seconds. |
| `C5_TELEMETRY_JSONL` | `true` | Write one JSONL event per decision and per order attempt to `logs/trade_events.jsonl` for observability. |
| `C5_POLY_EDGE_MIN` | `0.03` | Min edge (p − market price) to allow ML trades. 0 = disabled (not recommended). Snipe bypasses. |
| `C5_POLY_SNIPE_BET_MULTIPLIER` | `2.0` | Snipe trades bet N× normal size (higher accuracy → bigger bets) |
| `C5_POLY_TRADE_LEAD_SECONDS` | `30` | Seconds after a new 5-min window opens to place the main trade (gives Gamma time to list the market). |
| `C5_SNIPE_LEAD_SECONDS` | `10` | Seconds before window close to fire the snipe check/order. |

### How to validate execution improvements (1 hour)

Run the bot for ~1 hour in dry-run or live mode, then inspect `logs/trade_events.jsonl`.

Track these metrics:

- Skip counts by `reason_code` (especially `SKIP_NO_DEPTH`, `SKIP_SPREAD_TOO_WIDE`, `SKIP_TOO_LATE`)
- Orders placed: count of `ORDER_SUBMIT`
- Fill rate: ratio of `ORDER_FILL` / `ORDER_SUBMIT` (and `ORDER_PARTIAL` frequency)
- Average spread at entry: average `spread_bps` on `DECISION` events that led to `ORDER_SUBMIT`
- Slippage proxy: compare `avg_fill_price` (from reconciliation events) vs `best_ask.price` at submit time
- Win/loss: use existing resolved trade records, but confirm that unfilled outcomes show up as cancels/skips (no “ghost wins”)

### Feed & data stability — v0.4.10

These settings improve reliability and reduce missed windows.

| Setting | Default | What it does |
| ------- | ------- | ------------ |
| `C5_RTDS_JSON_PING_ENABLED` | `true` | Send JSON `PING` messages periodically to keep the RTDS WebSocket healthy (recommended). |
| `C5_RTDS_JSON_PING_INTERVAL_SEC` | `5` | RTDS JSON ping interval in seconds. |
| `C5_CHAINLINK_STALE_THRESHOLD_SEC` | `30` | Treat Chainlink price as stale if older than this many seconds (affects snipe + oracle alignment). |
| `C5_COINBASE_INCREMENTAL_CANDLES` | `true` | Fetch only missing candle tail (plus overlap) instead of refetching full lookback each run (faster, fewer failures). |

### Intelligence settings — v0.4.0

These control the bot's prediction pipeline. Most work automatically — only change if you know what you're doing.

| Setting | Default | What it does |
| ------- | ------- | ------ |
| `C5_ENSEMBLE_WEIGHT` | `0.6` | Blend ratio for predictions: 0.6 = 60% ML model + 40% live Chainlink delta. Higher = trust model more. Range 0.0–1.0. |
| `C5_QUIET_HOURS_UTC` | (blank) | Comma-separated UTC hours to skip ML trades (e.g. `3,4,5`). Snipe trades are never blocked. Leave blank = all hours active. |
| `C5_PAPER_STARTING_CASH` | `10000` | Virtual starting balance for Paper PnL in dry-run mode. Change this before enabling dry-run to simulate with a different bankroll. |

> **Platt calibration** and **hybrid training target** activate automatically — no settings to configure. The bot calibrates its probabilities when it has 30+ training samples, and switches to Chainlink-based training when 10+ oracle data points are collected.

### Risk rails (circuit breakers) — v0.3.0

Automated safety limits that pause trading when things go wrong. All configurable from the dashboard's **Risk Rails** section.

| Setting | Default | What it does |
| ------- | ------- | ------------ |
| `C5_RISK_DAILY_LOSS_PCT` | `10` | Pause trading after losing 10% of balance in any 24-hour window |
| `C5_RISK_CONSEC_LOSS_LIMIT` | `5` | Pause after 5 consecutive losing trades |
| `C5_RISK_UNFILLED_RATIO` | `0.5` | Pause if >50% of recent orders go unfilled |
| `C5_RISK_UNFILLED_LOOKBACK` | `20` | How many recent orders to check for fill rate |
| `C5_RISK_AUTO_RESUME_MINUTES` | `60` | Auto-resume after 60 min of pause (0 = manual only) |

Set any value to `0` to disable that specific rail. Risk state persists across restarts in `logs/risk_state.json`.

### Chainlink oracle alignment — v0.3.0

The bot connects to Polymarket's RTDS WebSocket and subscribes to the **exact same Chainlink BTC/USD oracle** Polymarket uses to resolve 5-minute markets. This eliminates the "oracle mismatch" problem from earlier versions where the bot predicted based on Coinbase but markets resolved based on Chainlink. If the Chainlink feed is temporarily unavailable, the bot falls back to Coinbase automatically.

### Expert / UNSAFE sizing

By default, percent sizing is capped:
- Normal: max 10% of balance per trade
- High-risk mode: max 50%
- Expert/UNSAFE mode: up to 100% (requires typing a confirmation phrase)

**Expert mode is extremely dangerous.** One bad trade could wipe your entire balance.

### Emergency actions

These are disabled by default for safety:

| Feature | Setting | What it does |
|---------|---------|--------------|
| Sell all positions | `C5_POLY_SELL_ALL_ENABLED=true` | Adds a "Sell All" button (requires confirmation typing) |
| Withdraw funds | `C5_WITHDRAW_ENABLED=true` | Enables withdrawing USDC to a specified address |

### Gas auto top-up

If you don't want to manually send gas:

1. Enable in dashboard: **Wallet care → Auto top-up gas** → Save
2. Add a 0x API key in `config/.env`: `C5_ZEROX_API_KEY=...`
   Get one from [dashboard.0x.org](https://dashboard.0x.org/)
3. Restart: `docker compose restart`

> Gas auto top-up needs a tiny amount of gas already in the wallet to work. It can't fix a wallet at zero gas.

---

## 14) FAQ & Troubleshooting

### Polymarket API Errors

**Q: "400 Bad Request" on /auth/api-key**
This means Polymarket rejected your wallet signature. It is almost always caused by one of three things:
1. **Clock Skew (Most Common):** Your VPS or computer's clock is out of sync. Polymarket is extremely strict about timestamps.
   * **Fix (Linux VPS):** Run `sudo chronyd -q` or `sudo ntpdate pool.ntp.org` to sync your clock.
   * **Fix (Windows):** Open Command Prompt as Administrator and run `w32tm /resync`.
2. **Wrong Signature Type:** You are using a MetaMask wallet (EOA) but set `C5_POLY_SIGNATURE_TYPE=1`, or you are using an Email/Google login but set it to `0`.
   * **Fix:** Go to Dashboard → Settings → Wallet and re-run the Auto-Detect tool.
3. **Wrong Funder Address:** You are using an Email/Google login but didn't provide the correct Proxy address from your Polymarket profile.

**Q: My trades say "Skipped (No Liquidity)" or "Unfilled"**
This is normal and means the bot protected your funds. 5-minute markets move fast and often have thin orderbooks. The bot uses FOK (Fill-Or-Kill) orders. If there isn't enough liquidity at the requested price, the order is instantly killed rather than leaving your money stuck on the orderbook.
* **Fix:** If you prefer to take the risk of your order resting on the book and potentially filling at a bad time, you can enable **Force GTC Orders** in Dashboard → Settings → Polymarket.

### Installation problems

**Q: "docker: command not found"**
Docker isn't installed. Go back to [Section 2](#2-installing-docker) and follow the steps for your operating system.

**Q: "Docker daemon is not running"**
Docker Desktop needs to be open. Find it in your Start menu (Windows) or Applications (Mac) and open it. Wait for the icon to stop animating before trying again.

**Q: "Permission denied" when running Docker on Linux**
Run: `sudo usermod -aG docker $USER` then log out and back in.

**Q: Windows says "WSL 2 installation is incomplete"**
Open PowerShell as Administrator (right-click → Run as Administrator) and run: `wsl --install`. Restart your PC.

**Q: "no matching manifest for windows/amd64"**
Docker Desktop is in Windows containers mode. Right-click the Docker icon in the system tray → click "Switch to Linux containers."

**Q: The build takes forever / seems stuck**
First build downloads ~500MB — this is normal. It can take 5–10 minutes on slow connections. After the first build, starts take ~5 seconds.

**Q: "container name already in use" error**
A previous container with the same name still exists. Remove it first, then rebuild:

```bash
docker rm -f crypto5min-polytrader
docker compose up -d --build
```

**Q: "Permission denied" when editing config/.env on a VPS**
Docker may have created the file as root. Use `sudo`:

```bash
sudo nano config/.env
```

Or write directly:

```bash
sudo bash -c 'cat >> config/.env << EOF
C5_POLY_SIGNATURE_TYPE=1
EOF'
```

### Dashboard problems

**Q: I can't access the dashboard**
1. Check the container is running: `docker ps` (you should see `crypto5min-polytrader`)
2. Make sure you're using the right port: `http://YOUR_IP:8602`
3. Check your firewall allows port 8602
4. If on a VPS: check the hosting provider's firewall/security group settings

**Q: The Setup Wizard keeps appearing**
Complete the wizard by following the `?token=...` URL it shows you. If the token is wrong, open `/setup` again in a fresh browser tab.

**Q: I changed settings but nothing happened**
Restart the container: `docker compose restart` — this forces a reload.

**Q: Dashboard data never updates**
The bot works on 5-minute windows. Wait up to 5 minutes. If still stuck, check logs: `docker logs crypto5min-polytrader --tail 20`

**Q: Dashboard returns 401 errors / "not authenticated" after a restart**
This is normal. The dashboard session key regenerates every time the container restarts, which logs everyone out. Just refresh the page and log in again with your dashboard password. Your data is not lost.

### Trading problems

**Q: Why is the signal taking so long to load / showing "---" for a while?**
The bot retrains its ML model every hour on fresh BTC price data. With 4 symbols active (BTC/ETH/SOL/XRP), training takes approximately 2 minutes per symbol — up to **~8 minutes total**. During this time the Signal card shows "training" or stale data. This is completely normal; the signal resumes automatically when training finishes. Tip: you can watch the logs to see when training completes: `docker logs crypto5min-polytrader --tail 20`.

> **v0.6.7 note:** Before this update, the training time was also causing the watchdog timer to fire and restart the bot every ~8 minutes. That's fixed — training now completes cleanly without any restarts.

**Q: Why are my wins so small? I'm winning but barely making any profit.**
This is expected behaviour in **Snipe mode** (the default). Here's why:
- Snipe fires at T-10 seconds before window close, when BTC has already clearly moved
- At that point Polymarket asks are priced at **$0.70–$0.95 per share** (the market already prices in the direction)
- Your payout is always $1.00 per share
- Profit per share = $1.00 − ask price = **$0.05–$0.30**

The tradeoff is high accuracy (~80–90%+). Small margins on many trades compound over time. Options to improve profit margins:
1. **Turn off Delta Pricing** (sidebar → Trading → Delta Pricing → Save) — relaxes the ask gate, allows trades at lower-confidence but cheaper prices
2. **Turn off Delta-First mode** (sidebar → Trading → Delta-First → Save) — re-enables ML directional trades which enter at ~$0.50/share (larger margin, but ~52–55% accuracy vs ~80–90%)
3. **Increase bet size** gradually once you're comfortable with the win rate

**Q: How do I get the bot to trade more frequently?**
By default with **Delta-First mode ON**, the bot's only entry is the late snipe at T-10s. Not every 5-minute window produces a large enough BTC move to trigger it — so some windows are skipped.

To get more trades:
1. **Turn off Delta-First mode** (sidebar → Trading → Delta-First → Save) — re-enables ML directional trades. Bot now has two entry paths: ML prediction entry + snipe. Expect 2–4× more trades, but lower average win rate (~55% vs ~85%).
2. **Lower confidence threshold** (sidebar → Signal → Threshold → try `0.50` or `0.52`). Works for ML trades.
3. **Turn off Delta Pricing** — the ask gate that blocks trades if asking price is too high relative to signal strength.

> **Important:** More trades = more exposure. Win rate may drop if you open all paths simultaneously. Always experiment with small bet sizes first.

**Q: The bot skips every window / never trades**
This is normal! The bot is being selective. Reasons it might skip:
- Confidence is below your threshold (try lowering it from 0.55 to 0.52)
- Kelly sizing computed zero edge — this happens when the model's confidence isn't higher than the live market price. **Fix: switch bet mode to `percent` (5-10%) in the dashboard sidebar.**
- Cooldown hasn't expired since last trade
- Market couldn't be found on Polymarket for this specific window
- Balance is too low for the minimum order size (5 shares × price ≈ $2.50+)

**Q: What are "ghost wins" / "win_unfilled"?**
Sometimes the bot places an order that doesn't fill on Polymarket's orderbook before the market resolves (e.g., the price moved too fast, or the orderbook was too thin). The bot detects these and tags them as `win_unfilled` or `loss_unfilled`. They're excluded from your real win rate because no money was gained or lost. On the dashboard's **Trades & Equity** tab, these appear as a dimmed **"W unfilled"** or **"L unfilled"** with a tooltip explaining what happened.

**v0.4.17+ thin orderbook guard:** optionally skip placing orders when there isn't enough cumulative liquidity to realistically fill your USDC size up to the FOK price cap. **Default OFF since v0.6.0** — FOK (Fill-or-Kill) orders handle thin books safely: they either fill instantly or are rejected with no cost. Enable if you prefer to skip thin markets entirely:
- `C5_POLY_REQUIRE_BOOK_DEPTH=true` (default: `false`)
- `C5_POLY_BOOK_DEPTH_MULT=1.10`

**Q: My orders keep getting canceled / never fill**
The bot now uses live CLOB pricing (not stale cached data) and retries up to 3 times. If orders still don't fill:
- Check your USDC balance — you need enough for at least 5 shares × price (about $2.50+)
- Fast-moving markets can jump past your price in seconds — this is normal
- The bot logs every attempt: check `docker logs crypto5min-polytrader --tail 50` for details

If you see lots of cancels due to odd pricing, try switching **Ask source**:
- `prefer_live` (default) usually improves fills when Gamma is stale-high.
- `legacy_max` can help if live book snapshots are occasionally missing.

**Q: "Key missing" error**
You need to set your Polymarket private key. The easiest way:
1. Go to `/reconfigure` in your browser (e.g. `http://YOUR_IP:8602/reconfigure`) to re-run the Setup Wizard
2. In Setup Wizard Step 2, paste your key and select wallet type
3. Or manually edit `config/.env` and add `C5_POLY_PRIVATE_KEY=0x...` then restart: `docker compose restart`

See [Section 7](#7-getting-your-polymarket-private-key) for how to get your private key.

**Q: "Low gas" warning**
Your wallet is low on POL/MATIC (the transaction fee token). Send ~$1–3 worth to your bot wallet address on Polygon (see [Section 8B](#b-gas-pol--matic--the-transaction-fee-token)).

**Q: "Insufficient balance" error**
Your USDC balance is lower than your max trade amount. Either add more USDC or lower `C5_POLY_MAX_USDC_PER_TRADE` in settings.

**Q: Dashboard shows $0 balance but I have funds on Polymarket**
This is almost always a **signature type mismatch**. If you signed up to Polymarket with **email or Google login**, you need to set your wallet type to Email/Google. Fix:

**Easiest way (v0.4.14+):**
1. Go to `/reconfigure` and open Setup Wizard Step 2
2. Set **Wallet type** to **Email / Google (MagicLink)**
3. Paste your **Funder Address** (your Polymarket profile address, not your private key)
4. Click **Save** — done, no restart needed

**Or manually:**
1. Edit your config: `nano config/.env` (or `sudo nano config/.env` on a VPS)
2. Add or change: `C5_POLY_SIGNATURE_TYPE=1`
3. If applicable, also set `C5_POLY_FUNDER_ADDRESS=` to your Polymarket deposit address
4. Restart: `docker compose restart`

> This is the **#1 most common issue** we see. If in doubt, try type `1` — it won't break anything if you switch back.

**Support checklist (copy/paste and ask the customer):**
1. What wallet login did you use on Polymarket: MetaMask wallet connection, or Email/Google?
2. What wallet type is selected in bot settings right now?
3. What exact `bot wallet` address is shown in the dashboard sidebar?
4. Did you send USDC on **Polygon** to that exact address?
5. Did you paste your private key from `reveal.magic.link/polymarket` into the **private key** field?
6. Did you paste a **wallet address** (not the private key) into the **funder address** field?
7. Can you share screenshot(s) of `/reconfigure` Step 2 (with private key partially hidden) plus the Polymarket profile address?

**Q: How do I know if I'm signature type 0 or 1?**
- **Type 0 (EOA):** You log into Polymarket by connecting a crypto wallet (MetaMask, Coinbase Wallet, etc.)
- **Type 1 (MagicLink/smart-contract):** You log into Polymarket with an **email address** or **Google account**

If you created your Polymarket account with email/Google, you are type `1`. Most users who set up via the browser "Sign in with Google" flow need type `1`.

**Q: Trades show in the bot but not on Polymarket**
Are you sure you're in **Live** mode (not Paper or Dry-run)? Check the mode indicator on the dashboard. In Dry-run, the bot logs "would trade" but doesn't actually place orders.

**Q: It looks like the bot is trading the previous 5-minute cycle (wrong market slug)**
Example: the bot shows `btc-updown-5m-1771432200` but Polymarket shows `btc-updown-5m-1771432500`.

This is almost always a **host clock drift** issue (common on Windows/WSL/VPS after sleep/resume). As of **v0.4.16**, the bot aligns window slugs to Polymarket's CLOB server time.

What to do:

1. Update to **v0.4.16+** (sidebar bottom-left → **↻ Check** → **Apply Update**)
2. Check `/api/window` — it now shows:
   - `slug` (Polymarket-aligned)
   - `local_slug` (what your machine clock would compute)
   - `time_offset_sec` (clock drift)
3. Make sure `C5_POLY_TIME_SYNC_ENABLED=true` in `config/.env` (default)
4. If you're on Windows/WSL, also ensure Windows time sync is enabled (Settings → Time & language → Date & time → Sync now)


### Wallet & funding problems

**Q: I sent USDC but the bot doesn't see it**
1. Did you send on **Polygon** network? (Not Ethereum!)
2. Wait 1–2 minutes for the transaction to confirm
3. Check your wallet on [polygonscan.com](https://polygonscan.com) — search your wallet address

**Q: I sent USDC on the wrong network (Ethereum instead of Polygon)**
Unfortunately, the bot can't access funds on Ethereum. You'll need to bridge them to Polygon using a service like [portal.polygon.technology](https://portal.polygon.technology/bridge). This requires gas on both networks.

**Q: How do I see my wallet address?**
It's shown on the dashboard sidebar under **"Wallet"** — a long string starting with `0x`. Click the 📋 button next to it to copy, or click the address to open it on Polygonscan. This is where you send USDC and POL gas.

**Q: I skipped the wallet step during setup — how do I add my key now?**
No need to start over! Two options:
1. Go to `/reconfigure` in your browser (e.g. `http://YOUR_IP:8602/reconfigure`) — this re-opens the Setup Wizard
2. In Setup Wizard Step 2, add your private key, wallet type, and funder address

### General questions

**Q: Can I run this on my laptop instead of a VPS?**
Yes — and the same applies to a **Windows desktop or Windows VPS**. Options:

- **Own PC / laptop:** The bot stops when you close your computer or it sleeps. For 24/7 operation, use a VPS or always-on computer.
- **Windows VPS:** Get a Windows Server VPS (e.g. [Vultr Windows ~$6/mo](https://www.vultr.com/?ref=9869564)), RDP in, install Docker Desktop, and run normally.

For 24/7 reliability, a Linux VPS on [Vultr](https://www.vultr.com/?ref=9869564), Hetzner, or DigitalOcean is the best option ($4-6/mo). See [Deployment Options](#deployment-options--pick-your-path) for all choices including Railway cloud deploy.

**Q: What are the minimum VPS specs?**
- **1 CPU, 1 GB RAM, 20 GB storage** is the minimum (works for most VPS providers' cheapest tier)
- Ubuntu 22.04 or 24.04 recommended
- Docker + Docker Compose must be installed (see [Section 2](#2-installing-docker))
- Popular choices: Hetzner CX22 ($4/mo), [Vultr Cloud Compute ($6/mo)](https://www.vultr.com/?ref=9869564), DigitalOcean Basic ($6/mo)
- **Windows VPS option:** [Vultr Windows Server (~$6/mo)](https://www.vultr.com/?ref=9869564) — RDP in, install Docker Desktop, done

**Q: I'm in the US — do I need a VPN?**
Polymarket restricts access from US IP addresses. If you're running on a **US-based VPS or local machine**, you'll need to either:
1. Use a **non-US VPS** (e.g., Hetzner in Germany, or any EU/Asia server)
2. Set up a VPN on your VPS that routes through a non-US location

Without this, the bot may hang during training/initialization or fail to place orders. If you see the bot stuck at "training" or getting connection errors, this is likely the reason.

**Q: How do I update the bot to the latest version?**
Use **one-click update in the dashboard** first:
1. In the sidebar bottom-left, click **↻ Check**
2. If an update is found, click **Apply Update**
3. Wait ~30 seconds, then refresh the page

If one-click update is unavailable in your environment, use ZIP/manual update:
1. `docker compose down`
2. Unzip the new version into a new folder
3. Copy `config/.env`, `logs/`, and `data/` into the new folder
4. `docker compose up -d --build`

If you get "container name already in use":
```bash
docker rm -f crypto5min-polytrader
docker compose up -d --build
```

**Q: Can I trade crypto other than BTC?**
Yes. Change `C5_SYMBOL` in `config/.env` to another Coinbase pair like `ETH-USD`. Note that Polymarket availability for different assets may vary.

**Q: How do I completely stop the bot?**
Run `docker compose down` in the bot folder. This stops and removes the container. Your settings and data are preserved in the `config/` and `logs/` folders.

**Q: How do I reset everything and start fresh?**
1. Stop: `docker compose down`
2. Delete `config/.env`, `logs/state.json`, and `logs/runtime_config.json`
3. Start: `docker compose up -d --build`
4. Complete the Setup Wizard again

**Q: Is this guaranteed to make money?**
**No.** No trading bot can guarantee profits. The ML model has ~52–55% accuracy, and snipe mode has higher accuracy but smaller margins. Markets are unpredictable. Only trade money you can afford to lose. Start small and scale up based on real results, not backtests.

**Q: Do I need a Polymarket account?**
The bot creates/uses a crypto wallet for Polymarket's CLOB (central limit order book) API. You don't need a regular Polymarket login, but you DO need a private key from a Polymarket-linked wallet. See [Section 7](#7-getting-your-polymarket-private-key).

---

## Still stuck?

Reach out via **Whop messaging** (from the account you used to purchase). Include:

1. What you're trying to do
2. What error you see (screenshot or copy-paste)
3. Your operating system (Windows/Mac/Linux)
4. Output of `docker logs crypto5min-polytrader --tail 30`
