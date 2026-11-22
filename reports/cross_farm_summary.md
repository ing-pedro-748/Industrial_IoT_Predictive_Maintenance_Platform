# Cross-Farm LOTO Summary (Phase 2)

## Method
- LOTO per farm, rolling features (6/36 steps), z-score threshold calibrated per fold.
- Features per farm (pilot set, 6 sensors each).

## Z-score (rolling + calibrated) aggregates

| Farm | Turbines | Events | Precision | Recall | F1 | False alarms/day | Event detection rate |
|---|---|---|---|---|---|---|---|
| A | 5 | 22 | 0.420 | 0.690 | 0.514 | 14.76 | 1.0 |
| B | 9 | 15 | 0.407 | 0.474 | 0.433 | 59.56 | 1.0 |
| C | 22 | 58 | 0.348 | 0.515 | 0.388 | 21.41 | 1.0 |

## Isolation Forest (contamination 0.15) aggregates

| Farm | Precision | Recall | F1 | False alarms/day | Event detection rate |
|---|---|---|---|---|---|
| A | 0.464 | 0.228 | 0.293 | 3.24 | 1.0 |
| B | 0.397 | 0.093 | 0.150 | 12.46 | 1.0 |
| C | 0.350 | 0.153 | 0.167 | 2.48 | 0.667 |

## Observations
- Z-score with rolling features generalizes across farms with F1 0.39-0.51.
- Farm C has lower precision (0.348) and high false alarms (21.4/day).
- IF event detection rate drops on Farm C (0.667 at 0.15), suggesting the
  pilot features or contamination prior are not transferable.
- Farm B has very high false alarms (59.56/day) for z-score, likely due to
  noisier sensors or threshold miscalibration.

## Recommendations
- Refine feature sets per farm (more sensors, better equivalence).
- Calibrate thresholds with cost-aware objectives per farm.
- Investigate Farm C IF miss (event detection 0.667).
- Add MLflow tracking before scaling experiments.
