# Baseline Statistical Results (Phase 2)

## Method
- Z-score per feature using train-portion (train_test=='train') statistics.
- Flag row if any pilot feature |z| > threshold.
- Pilot features (Farm A): sensor_0_avg (ambient temp), wind_speed_3_avg,
  sensor_5_avg (pitch), power_30_avg, sensor_11_avg (gearbox temp),
  sensor_13_avg (generator temp).

## Aggregate (all 22 Farm A events, prediction window)

| threshold | precision | recall | f1 | false_alarms/day |
|---|---|---|---|---|
| 2.0 | 0.504 | 0.290 | 0.368 | 15.76 |
| 2.5 | 0.555 | 0.154 | 0.241 | 6.83 |
| 3.0 | 0.605 | 0.114 | 0.191 | 4.11 |
| 3.5 | 0.631 | 0.100 | 0.173 | 3.24 |

## Per-event results
See `reports/baseline_results.csv` (22 events).

## Observations
- Precision is high (0.7-1.0) on many anomaly events, but recall is low
  (anomalies are sparse within the prediction window).
- Normal series produce 0-4 false alarms/day at threshold 3.0.
- Threshold 2.0 best F1 but 4x more false alarms.
- Detection lead time varies: some events detected days before event_start,
  others only after (negative lead time).

## Next steps
- Try per-turbine thresholds and multivariate (Isolation Forest).
- Add window-based aggregation features (rolling mean/std).
- Evaluate across turbines (leave-one-turbine-out).
- Log experiments in MLflow (Phase 6).
