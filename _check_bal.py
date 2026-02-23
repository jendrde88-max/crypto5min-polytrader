"""Quick balance check script — run inside container."""
import os, sys
sys.path.insert(0, '/app/src')
from dotenv import load_dotenv
load_dotenv('/app/config/.env', override=False)

from py_clob_client.client import ClobClient
from py_clob_client.clob_types import AssetType, SignatureType, BalanceAllowanceParams

pk = os.environ.get('C5_POLY_PRIVKEY', '')
if not pk:
    print("ERROR: C5_POLY_PRIVKEY not set")
    sys.exit(1)

c = ClobClient('https://clob.polymarket.com', key=pk, chain_id=137)
r = c.get_balance_allowance(params=BalanceAllowanceParams(
    asset_type=AssetType.COLLATERAL,
    signature_type=SignatureType.EOA,
))
print(f"USDC balance:    ${float(r.get('balance', 0)) / 1e6:.4f}")
print(f"USDC allowance:  ${float(r.get('allowance', 0)) / 1e6:.4f}")
print(f"Raw response: {r}")
