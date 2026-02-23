import json
data = json.loads(open('/app/logs/poly_ops.json', encoding='utf-8-sig').read())
redeems = [x for x in data if x.get('type') == 'redeem' and x.get('tx_hash')]
print(f"Total confirmed redeems: {len(redeems)}")
total = sum(r.get('usdc_received', 0) or 0 for r in redeems)
print(f"Total USDC redeemed: ${total:.4f}")
print()
for r in redeems[-8:]:
    print(r.get('ts_iso','')[:19], f"${r.get('usdc_received','?')}", r.get('tx_hash',''))
