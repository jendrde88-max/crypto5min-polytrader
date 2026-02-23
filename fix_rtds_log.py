"""Update the log message after changing SUBSCRIBE_MSG filters."""
import pathlib

for p in [
    pathlib.Path('/root/crypto5min-polytrader/src/crypto5min_polytrader/chainlink_feed.py'),
    pathlib.Path('/app/src/crypto5min_polytrader/chainlink_feed.py'),
]:
    if not p.exists():
        continue
    t = p.read_text()
    old_log = "subscribed to btc/usd"
    new_log = "subscribed (all assets, client-side btc filter)"
    if old_log in t:
        t = t.replace(old_log, new_log)
        p.write_text(t)
        print(str(p) + ': log message updated')
    else:
        print(str(p) + ': already updated or not found')
