import json, time

trades = json.load(open("/app/logs/poly_trades.json"))
now = time.time()

filled = [t for t in trades if t.get("order_status") == "filled"]
wins = [t for t in trades if t.get("resolved") == "win"]
losses = [t for t in trades if t.get("resolved") == "loss"]
redeemed = [t for t in trades if t.get("redeem_status") == "success"]
pending_resolve = [t for t in filled if not t.get("resolved")]

print(f"=== BOT STATUS (v0.4.7) ===")
print(f"Total trades: {len(trades)}")
print(f"Filled: {len(filled)} | Canceled/unfilled: {len(trades) - len(filled)}")
print(f"Resolved: {len(wins)} win, {len(losses)} loss")
print(f"Redeemed on-chain: {len(redeemed)}")
print(f"Pending resolution: {len(pending_resolve)}")

# Last filled trade
if filled:
    last = filled[-1]
    age = int(now - last.get("placed_ts", 0))
    print(f"\nLast filled trade:")
    print(f"  {last.get('window_slug')} dir={last.get('direction')}")
    print(f"  filled=${last.get('filled_size',0):.2f} resolved={last.get('resolved')} redeem={last.get('redeem_status')}")
    print(f"  {age//60} min ago")

# Recent activity
recent_1h = [t for t in trades if now - t.get("placed_ts", 0) < 3600]
recent_filled_1h = [t for t in filled if now - t.get("placed_ts", 0) < 3600]
print(f"\nLast 1h: {len(recent_1h)} attempts, {len(recent_filled_1h)} filled")

# P&L from filled trades
total_bet = sum(t.get("usdc", 0) for t in filled)
total_won = sum(t.get("filled_size", 0) for t in wins)
total_lost = sum(t.get("usdc", 0) for t in losses)
print(f"\nTotal wagered: ${total_bet:.2f}")
print(f"Won: ${total_won:.2f} from {len(wins)} wins")
print(f"Lost: ${total_lost:.2f} from {len(losses)} losses")
if total_bet > 0:
    pnl = total_won - total_lost
    print(f"Net P&L: ${pnl:+.2f}")
