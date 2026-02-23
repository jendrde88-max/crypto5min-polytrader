import json

trades = json.load(open('logs/poly_trades_remote.json'))

# Find wins without successful redeem
no_redeem_wins = [t for t in trades if t.get('resolved') == 'win' and t.get('redeem_status') != 'success']
print(f'Wins without successful redeem: {len(no_redeem_wins)}')
unredeemed_value = 0
for t in no_redeem_wins:
    resp = t.get('response', {})
    status = resp.get('status', '') if isinstance(resp, dict) else ''
    taking = float(resp.get('takingAmount', 0)) if isinstance(resp, dict) else 0
    slug = t.get('window_slug', '?')
    order = t.get('order_status', '?')
    redeem = t.get('redeem_status', 'none')
    unredeemed_value += taking
    print(f"  {slug} order={order} resp={status} redeem={redeem} shares={taking}")

print(f"\nTotal unredeemed win shares: {unredeemed_value:.2f}")
print(f"(These shares are worth ${unredeemed_value:.2f} if redeemed)")

# Also check: losses without redeem? (losses can't be redeemed, just checking)
# And check overall account balance reconciliation
total_deposited_estimate = 229.67  # from first equity point
wins_redeemed = [t for t in trades if t.get('resolved') == 'win' and t.get('redeem_status') == 'success']
print(f"\n=== Summary ===")
print(f"Total trades: {len(trades)}")
print(f"Wins: {sum(1 for t in trades if t.get('resolved')=='win')}")
print(f"Losses: {sum(1 for t in trades if t.get('resolved')=='loss')}")
print(f"Win unfilled: {sum(1 for t in trades if t.get('resolved')=='win_unfilled')}")
print(f"Redeemed wins: {len(wins_redeemed)}")
print(f"Unredeemed wins: {len(no_redeem_wins)}")
print(f"Current balance: $1.40")
print(f"Unredeemed value: ${unredeemed_value:.2f}")
print(f"Effective equity: ${1.40 + unredeemed_value:.2f}")
