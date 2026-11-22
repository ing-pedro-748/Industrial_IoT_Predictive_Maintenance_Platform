# Model Comparison — Phase 2

## Z-score baseline (threshold 2.0, aggregate)
- Precision: 0.504 | Recall: 0.290 | F1: 0.368 | False alarms/day: 15.76

## Isolation Forest (contamination 0.10, single event 0)
- Precision: 0.471 | Recall: 0.261 | F1: 0.336 | False alarms/day: 29.45

## Isolation Forest (contamination 0.15, single event 0)
- Precision: 0.590 | Recall: 0.450 | F1: 0.510 | False alarms/day: 31.45

## Isolation Forest (aggregate, 22 events, contamination 0.05)
- Precision: 0.726 | Recall: 0.104 | F1: 0.164 | False alarms/day: 4.84

## Observations
- IF has higher precision and fewer false alarms in aggregate, but lower recall.
- Z-score at threshold 2.0 has better recall and F1 on the aggregate.
- Neither model achieves strong recall; anomalies are sparse and subtle.
- Contamination parameter strongly affects IF recall/precision trade-off.

## Next steps
- Add rolling window features (mean, std, min, max over 1h/6h) to capture dynamics.
- Evaluate per-turbine thresholds.
- Consider multivariate IF with window features.
- Log best configs in MLflow when available.
