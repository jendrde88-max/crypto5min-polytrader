# Support

For help installing or troubleshooting:

1) Read `SETUP_GUIDE.md`
2) Check `METRICS_AND_CAVEATS.md`
3) If still stuck, contact support via **Whop** (message from the account used to purchase)

## What to include in a support request

- Your OS (Windows/Linux/macOS)
- Whether you are using Docker Desktop or a VPS
- A screenshot of the dashboard error (if any)
- The last 100 lines of container logs (do **not** include private keys)

## FAQ

### The dashboard says “Low gas” — what do I do?

Send a small amount (about **$1–$3**) of **POL/MATIC** to your bot wallet.

Your bot wallet address is shown in the **dashboard sidebar under "Wallet."** Click the 📋 button to copy it, or click the address to view it on Polygonscan.

The "Auto top-up gas" feature is optional/advanced. If you want to use it, you'll need a 0x API key.

See `SETUP_GUIDE.md` → "Gas (POL/MATIC) + optional auto top-up".

### I skipped the wallet setup during installation — how do I fix it?

Go to `/reconfigure` in your browser (e.g. `http://YOUR_IP:8602/reconfigure`) to re-run the Setup Wizard, then fill **Step 2 (Wallet)**.

### The dashboard shows $0 balance but I have funds on Polymarket

You probably need to set your wallet type. If you signed up to Polymarket with **email or Google**, go to `/reconfigure` and set **Step 2 → Wallet type** to **Email / Google (MagicLink)**. See `SETUP_GUIDE.md` → Section 7B for details.

### Copy/paste intake questions for "$0 balance" tickets

Send these exact questions to the customer:

1. Did you create/login your Polymarket account using **MetaMask** or **Email/Google**?
2. In `/reconfigure` Step 2, what wallet type is selected right now?
3. What is the **bot wallet address** shown in your dashboard sidebar?
4. Did you send USDC on **Polygon** to that exact address?
5. In the wallet form, did you paste your `reveal.magic.link` value into **Private Key**?
6. In the wallet form, did you paste a **wallet address** (not private key) into **Funder Address**?
7. Please share screenshots of:
   - `/reconfigure` Step 2 (hide most of the private key)
   - Polymarket profile address
   - Wallet balance page / transaction hash

Quick triage rule:
- If login type is Email/Google, wallet type should usually be `Email / Google` and funder must be a 42-char `0x...` address.
- If login type is MetaMask direct, wallet type should be `MetaMask` and funder is usually blank.

### Paper PnL / Virtual Balance

**Q: What is the Paper Balance on the dashboard?**
When you're in Dry-Run mode, the bot tracks a virtual USDC balance. Every trade is "paper filled" at the ask price, and when markets resolve, your virtual balance updates. You'll see Paper Balance, P&L, and Win Rate in the sidebar.

**Q: How do I change the starting balance?**
Set `C5_PAPER_STARTING_CASH` in your `.env` file (default: 10000). Or use the "Set" button next to the starting cash display on the dashboard. Changing the starting cash resets your paper ledger.

**Q: How do I reset my paper balance?**
Click "Reset Paper Balance" on the dashboard sidebar (visible in dry-run mode). This resets your cash to the starting amount and clears all virtual trades.

---

Support is provided via Whop messaging.
