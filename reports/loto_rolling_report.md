# LOTO with Rolling Features and Threshold Calibration (Phase 2)

## Change from baseline LOTO
- Added rolling window features (6 and 36 steps = 1h and 6h) for mean/std of each
  pilot sensor, shifted by 1 to avoid leakage.
- Z-score threshold calibrated per fold on a time-based validation split
  (candidates 1.5-4.0, best F1).
- IF uses contamination-based prediction (threshold calibration disabled after
  producing 0 predictions).

## Aggregate results (5 folds)

| Variant | Precision | Recall | F1 | False alarms/day | Event detection rate |
|---|---|---|---|---|---|
| Z-score baseline (thr 2.0) | 0.475 | 0.323 | 0.377 | 5.47 | 1.0 |
| Z-score + rolling + calibrated (thr 1.5) | 0.420 | 0.690 | 0.514 | 14.76 | 1.0 |
| IF 0.15 (rolling) | 0.464 | 0.228 | 0.293 | 3.24 | 1.0 |
| IF 0.10 (rolling) | 0.429 | 0.138 | 0.194 | 1.88 | 1.0 |

## Observations
- Rolling features substantially improve Z-score recall (0.32 -> 0.69) and F1
  (0.377 -> 0.514), at the cost of more false alarms (5.47 -> 14.76/day).
- Calibrated threshold (1.5) is lower than the fixed 2.0, trading precision for
  recall.
- IF does not benefit as much; F1 0.293 (0.15) vs 0.347 in baseline LOTO.
- Event detection rate remains 1.0 for all variants except IF 0.05 (0.867).

## Trade-off
- High recall (0.69) with 14.8 false alarms/day may be acceptable for
  safety-critical monitoring; for cost-sensitive maintenance, threshold 2.0-2.5
  balances better.

## Next steps
- Calibrate thresholds on a cost-aware objective (e.g., maximize F1 or minimize
  false alarms subject to recall >= 0.5).
- Add more feature types (min/max, lag differences).
- Extend to Farms B/C after schema equivalence.
- Begin MLflow tracking (Phase 6).
