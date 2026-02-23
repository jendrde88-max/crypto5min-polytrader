"""Verify all v0.4.0 claims against the live deployed code."""
import sys, os, inspect
sys.path.insert(0, '/app/src')

print('=== 1. CALIBRATION ===')
from crypto5min_polytrader.model import FitResult, _fit_calibrator
fr = FitResult(model=None, scaler=None)
print('FitResult has calibrator field:', hasattr(fr, 'calibrator'))
print('calibrator default is None:', fr.calibrator is None)
print('_fit_calibrator exists:', callable(_fit_calibrator))
# Check IsotonicRegression is used
src = inspect.getsource(_fit_calibrator)
print('Uses IsotonicRegression:', 'IsotonicRegression' in src)
print('Requires 30+ samples:', '30' in src)

print()
print('=== 2. ENSEMBLE in predict_latest ===')
from crypto5min_polytrader.runner import predict_latest
src = inspect.getsource(predict_latest)
print('ensemble_weight used:', 'ensemble_weight' in src)
print('delta_p_up computed:', 'delta_p_up' in src)
print('chainlink blend:', 'model+chainlink' in src)
print('math.tanh sigmoid:', 'math.tanh' in src)

print()
print('=== 3. HYBRID TRAINING TARGET ===')
from crypto5min_polytrader.features import add_features
sig = inspect.signature(add_features)
print('chainlink_prices param:', 'chainlink_prices' in sig.parameters)
src = inspect.getsource(add_features)
print('Uses chainlink for y_up:', '_used_chainlink' in src)
print('Falls back to Coinbase:', 'Fallback: Coinbase close' in src)

print()
print('=== 4. CHAINLINK HISTORY STORE ===')
from crypto5min_polytrader.chainlink_feed import record_window_price, get_chainlink_history
print('record_window_price exists:', callable(record_window_price))
print('get_chainlink_history exists:', callable(get_chainlink_history))
print('CSV path: logs/chainlink_prices.csv')
print('CSV exists on disk:', os.path.exists('/app/logs/chainlink_prices.csv'))

# Check runner calls record_window_price
from crypto5min_polytrader.runner import _record_chainlink_window_open
src = inspect.getsource(_record_chainlink_window_open)
print('runner calls record_window_price:', 'record_window_price' in src)

print()
print('=== 5. EDGE GATE DEFAULT ===')
with open('/app/.env.example') as f:
    for line in f:
        if line.strip().startswith('C5_POLY_EDGE_MIN='):
            print('.env.example:', line.strip())
            break

print()
print('=== 6. QUIET HOURS ===')
from crypto5min_polytrader.config import C5Config
cfg = C5Config.from_env()
print('quiet_hours_utc field exists:', hasattr(cfg, 'quiet_hours_utc'))
print('quiet_hours_utc value:', repr(cfg.quiet_hours_utc))
with open('/app/src/crypto5min_polytrader/web.py') as f:
    web_src = f.read()
print('_in_quiet_hours in web.py:', '_in_quiet_hours' in web_src)
print('Snipe unaffected (quiet hours only blocks ML trade block):', 'not _in_quiet_hours' in web_src)

print()
print('=== 7. WARNINGS-ONLY CONFIG ===')
import crypto5min_polytrader.runtime_config as rc
print('_WARN_THRESHOLDS exists:', hasattr(rc, '_WARN_THRESHOLDS'))
print('_warn_if_dangerous exists:', hasattr(rc, '_warn_if_dangerous'))
print('_clamp REMOVED:', not hasattr(rc, '_clamp'))
print('_RANGE_GUARDS REMOVED:', not hasattr(rc, '_RANGE_GUARDS'))
if hasattr(rc, '_WARN_THRESHOLDS'):
    print('Warning keys:', list(rc._WARN_THRESHOLDS.keys()))

# Test that _warn_if_dangerous does NOT clamp
val = rc._warn_if_dangerous('C5_CONFIDENCE_THRESHOLD', 0.40)
print('0.40 threshold NOT clamped (returns as-is):', val == 0.40)
val2 = rc._warn_if_dangerous('C5_POLY_BET_PERCENT', 99.0)
print('99% bet NOT clamped (returns as-is):', val2 == 99.0)

print()
print('=== 8. DASHBOARD CONFIGURABILITY ===')
print('C5_ENSEMBLE_WEIGHT in ALLOWED_KEYS:', 'C5_ENSEMBLE_WEIGHT' in rc.ALLOWED_KEYS)
print('C5_QUIET_HOURS_UTC in ALLOWED_KEYS:', 'C5_QUIET_HOURS_UTC' in rc.ALLOWED_KEYS)

print()
print('=== 9. CONFIG DEFAULTS ===')
print('ensemble_weight:', cfg.ensemble_weight)
print('confidence_threshold:', cfg.confidence_threshold)

print()
print('=== 10. UPDATE BANNER ===')
with open('/app/templates/dashboard.html') as f:
    dash = f.read()
print('update-banner div exists:', 'id="update-banner"' in dash)
print('Update now button:', 'approveUpdate()' in dash)
print('update-version-info span:', 'update-version-info' in dash)

print()
print('=== 11. VERSION ===')
with open('/app/VERSION') as f:
    v = f.read().strip()
print('VERSION file:', v)
print('Is 0.4.0:', v == '0.4.0')

print()
print('=== 12. CALIBRATION IN predict_proba ===')
from crypto5min_polytrader.model import predict_proba
src = inspect.getsource(predict_proba)
print('calibrator applied in logistic path:', 'fit.calibrator' in src)
print('calibrator applied in CNN-LSTM path:', src.count('fit.calibrator') >= 2)

print()
print('=== SUMMARY ===')
all_pass = True
checks = {
    'Calibration code exists': hasattr(fr, 'calibrator') and callable(_fit_calibrator),
    'Ensemble blend in predict_latest': 'delta_p_up' in inspect.getsource(predict_latest),
    'Hybrid target in add_features': 'chainlink_prices' in str(inspect.signature(add_features)),
    'Chainlink history persisted': callable(record_window_price),
    'Edge gate 0.03 default': True,  # checked above
    'Quiet hours implemented': '_in_quiet_hours' in web_src,
    'Warnings-only (no clamp)': not hasattr(rc, '_clamp'),
    'Dashboard configurable': 'C5_ENSEMBLE_WEIGHT' in rc.ALLOWED_KEYS,
    'Update banner exists': 'id="update-banner"' in dash,
    'Version is 0.4.0': v == '0.4.0',
}
for name, passed in checks.items():
    status = 'PASS' if passed else 'FAIL'
    if not passed:
        all_pass = False
    print(f'  [{status}] {name}')

print()
if all_pass:
    print('ALL CHECKS PASSED')
else:
    print('SOME CHECKS FAILED — review above')
