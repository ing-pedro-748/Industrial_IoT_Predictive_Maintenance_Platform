# LOTO Evaluation Report (Phase 2)

## Method
- Leave-One-Turbine-Out on Farm A (5 turbines: 0, 10, 11, 13, 21).
- For each fold, train on the other 4 turbines (train portions only),
  evaluate on the held-out turbine (prediction portions).
- Z-score: stats from training turbines, threshold 2.0.
- Isolation Forest: contamination 0.05 / 0.10 / 0.15.
- No data leakage: stats/model fit only on training turbines.

## Aggregate results (5 folds)

| Model | Contamination | Precision | Recall | F1 | False alarms/day | Event detection rate |
|---|---|---|---|---|---|---|
| Z-score | — | 0.475 | 0.323 | 0.377 | 5.47 | 1.0 |
| IF | 0.05 | 0.448 | 0.107 | 0.171 | 1.40 | 1.0 |
| IF | 0.10 | 0.470 | 0.211 | 0.285 | 3.27 | 1.0 |
| IF | 0.15 | 0.466 | 0.288 | 0.347 | 5.05 | 1.0 |

## Per-turbine F1

| Turbine | Z-score | IF 0.15 |
|---|---|---|
| 0 | 0.459 | 0.465 |
| 10 | 0.485 | 0.475 |
| 11 | 0.308 | 0.193 |
| 13 | 0.361 | 0.334 |
| 21 | 0.272 | 0.268 |

## Observations
- Event detection rate = 1.0 for all folds: every anomaly event produced at least
  one alarm.
- Turbine 11 is consistently hardest (lowest F1 for both models).
- Turbine 10 is easiest.
- Z-score (thr 2.0) has best aggregate F1 (0.377) and recall (0.323).
- IF at 0.15 is competitive on F1 (0.347) with similar false-alarm rate.
- Avg lead time is negative on average (alarms tend to occur after event_start),
  suggesting the models react rather than predict early.

## Limitations
- Only 5 turbines / 22 events; small sample.
- No rolling features yet; point-wise z-scores miss temporal dynamics.
- Thresholds fixed (not calibrated per fold on validation data).
- Contamination for IF is a global prior, not turbine-specific.

## Recommendations
- Add rolling window features (1h/6h) and re-run LOTO.
- Calibrate thresholds on a validation split per fold.
- Investigate turbine 11 (possible sensor differences or noisier data).
- Extend to Farms B and C after schema equivalence.
