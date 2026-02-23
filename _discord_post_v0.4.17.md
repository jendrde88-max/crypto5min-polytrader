# 🚀 Crypto5min PolyTrader v0.4.17 is live

Big update — better fills, better timing, better setup:

✅ **Thin orderbook guard (default ON)**

- Reduces "**W/L unfilled**" (ghost wins) caused by thin Polymarket liquidity
- Before placing an order, the bot checks **cumulative live orderbook depth** up to its FOK worst-price cap
- If there isn't enough liquidity to fill your USDC size (with a cushion), it **skips** instead of placing a trade that can't fill

⏱️ **Window time sync**

- Bot now syncs its 5-minute window clock to **Polymarket's CLOB server time**
- Fixes "previous cycle" trades caused by clock drift (common on Windows/WSL/VPS after sleep)
- Falls back to local time if the server is temporarily unreachable

🔒 **Wallet setup validation**

- Setup wizard now **validates your private key** before saving — catches bad keys immediately
- Funder address field rejects private keys pasted by mistake (must be a `0x...` wallet address)
- Clear error messages in the dashboard if something's wrong

🖥️ **Multi-bot VPS support**

- `docker-compose.yml` now uses `C5_DASHBOARD_PUBLIC_PORT` for the public port mapping
- If `:8602` is already taken (copybot), set `C5_DASHBOARD_PUBLIC_PORT=8603`
- Auto-updater tries multiple ports to find the update server

🔧 **New settings**

- `C5_POLY_REQUIRE_BOOK_DEPTH=true` / `C5_POLY_BOOK_DEPTH_MULT=1.10` — thin orderbook guard
- `C5_POLY_TIME_SYNC_ENABLED=true` — window time sync (default on)

📦 Update via the dashboard's **Check for updates** button (recommended), or download the new ZIP from Whop.

If anyone still sees unfilled trades after this update, DM me a screenshot of the Trades tab + your last 50 log lines and I'll dig in.
