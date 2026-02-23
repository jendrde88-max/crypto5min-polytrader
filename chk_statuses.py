import json
from collections import Counter

data = json.load(open('/app/logs/poly_trades.json'))
statuses = Counter(t.get('status', 'none') for t in data)
print("Status distribution:", dict(statuses))
print()

# Show "filled" but not redeemed/loss
for s in ['filled', 'placed', 'open', 'pending', 'won', 'none', None]:
    candidates = [t for t in data if t.get('status') == s]
    if candidates:
        basis = sum(float(t.get('cost_basis') or t.get('amount_usdc') or 0) for t in candidates)
        print(f"Status='{s}': {len(candidates)} trades, basis=${basis:.2f}")
        for t in candidates[-5:]:
            slug = (t.get('market_slug') or '')[:45]
            b = float(t.get('cost_basis') or t.get('amount_usdc') or 0)
            print(f"  {slug} | ${b:.2f} | filled={t.get('filled')}")
