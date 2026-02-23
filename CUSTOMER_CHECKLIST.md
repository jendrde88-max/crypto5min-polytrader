# Customer checklist (before you click LIVE)

1. Install + run the dashboard

    - Follow `SETUP_GUIDE.md`
    - Confirm you can log in and see the Signal updating

2. Check your wallet address

    - Your bot wallet address is shown in the dashboard sidebar under **Wallet**
    - Click the 📋 button to copy it — this is where you'll send USDC and gas (POL)
    - If it's not showing, go to `/reconfigure` or **Settings → Wallet** to add your key

3. Read the caveats

    - `METRICS_AND_CAVEATS.md`
    - `legal/RISK_DISCLOSURE.md`

4. Start in PAPER

    - Let it run for a while and confirm stability

5. Then DRY-RUN

    - Set `C5_MODE=polymarket` and keep `C5_POLY_DRY_RUN=true`
    - Confirm the bot finds markets and logs planned trades
    - Your dashboard will show **Paper Balance** — the bot tracks virtual fills and P&L so you can evaluate performance before going live

6. Live (small)

    - Start with `C5_POLY_MAX_USDC_PER_TRADE=2`–`5`
    - Keep `C5_POLY_BET_MODE=fixed`
    - Only increase limits after you understand the behavior

7. If anything looks wrong

    - Use Pause/Stop
    - Close positions in Polymarket UI if needed

Notes:

- Winning trades are automatically redeemed on-chain every 5 minutes.
- If a redeem tx fails, it retries automatically on the next cycle.
- Your settings, trade history, and balance are preserved during updates.
- **Skipped a step during setup?** Go to `/reconfigure` to re-run the wizard anytime.
- **Need to change your wallet key or type?** Use **Settings → Wallet** on the dashboard — no restart required.
