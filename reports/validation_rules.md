# Validation Rules

1. Schema: required meta columns present; sensor columns match farm schema.
2. No duplicate `time_stamp` or `id` within a file.
3. Timestamps parseable; frequency median = 10 min.
4. Gaps > 10 min must be recorded, not silently filled.
5. Nulls: record positions; do not impute in this phase.
6. Inf values: must be 0 (flag if not).
7. Constant columns: flag (asset_id expected; others investigate).
8. Zeros: distinguish legitimate (status, idling) from placeholder sensors.
9. Outliers: do not remove without justification (may be anomalies).
10. `train_test` must only take `train`/`prediction`.
11. `status_type_id` in {0..5}.
12. Event ids in event_info must exist as dataset files.
