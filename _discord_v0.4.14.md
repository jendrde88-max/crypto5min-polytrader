# Discord Announcement — v0.4.14

Copy everything below the line into Discord:

---

# 🚀 Crypto5min PolyTrader — v0.4.14 Update

Hey everyone! New update is live. This one fixes the most common setup issues people have been hitting.

## What's new

### 🔑 Wallet address now visible on the dashboard
Your bot wallet address is now displayed right in the sidebar — with a **copy button** and a **link to Polygonscan**. No more guessing where to send your gas (POL) or USDC.

### 🔄 Re-run the Setup Wizard anytime
Skipped a step during setup? No problem. Go to `/reconfigure` in your browser (e.g. `http://YOUR_IP:8602/reconfigure`) and the Setup Wizard opens back up — no need to reset your password or start over.

### ⚙️ Wallet Settings on the dashboard
New **Settings → Wallet** section lets you update your private key, wallet type (MetaMask vs Email/Google), and funder address — right from the dashboard. Changes apply instantly, no restart needed.

### 📋 Better error messages
- "Low gas" warning now **shows your actual wallet address** so you know exactly where to send POL
- "Withdraw is not set up yet" now **links directly to /reconfigure** instead of being a dead-end
- "Key missing" messages now **link to the setup wizard** instead of just telling you to edit a file

## How to update

**If you're on a VPS with the one-click updater:**
The update will show up automatically — just click "Apply Update" on the dashboard.

**If you're using the ZIP from Whop:**
1. Download the new ZIP (`Crypto5min_PolyTrader_v0.4.14.zip`) from Whop
2. Unzip into a **new folder** (don't overwrite your old one)
3. Run the update script to carry over your settings:

   **Linux/Mac:**
   ```
   bash update.sh /path/to/old/folder
   ```
   **Windows (PowerShell):**
   ```
   .\update.ps1 -OldPath "C:\path\to\old\folder"
   ```
4. Or manually copy `config/.env` and `logs/` from old → new, then:
   ```
   docker compose up -d --build
   ```

Your settings, trade history, and balance are all preserved during updates.

## Common setup issues this fixes

**"I skipped the wallet step and now I can't go back"**
→ Go to `http://YOUR_IP:8602/reconfigure`

**"It says low gas but I don't know where to send POL"**
→ Your wallet address is now in the sidebar with a copy button

**"Dashboard shows $0 balance but I have money on Polymarket"**
→ Go to Settings → Wallet, set type to "Email / Google (MagicLink)" and paste your funder address

**"It says withdraw is not set up yet — what do I do?"**
→ That message now links directly to `/reconfigure` so you can fix it

**"I can't log in — my password had $ or # in it"**
→ Fixed in this update. Passwords with special characters (`$`, `#`, `"`, `\`) now work correctly. If you're still locked out, SSH into your server and edit `config/.env` — change `C5_DASHBOARD_PASSWORD=` to a simpler password (letters + numbers only), then `docker compose down && docker compose up -d`.

## Quick reminder

⚠️ **This is for the Crypto5min PolyTrader bot only** (the automated BTC 5-min trading bot). This is NOT the Discord copy-trading bot — those are separate products.

Questions? Drop them in the support channel or message on Whop. 🙌
