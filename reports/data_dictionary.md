# Data Dictionary — CARE to Compare V6

## Meta columns
- `time_stamp`: measurement timestamp (10-min), anonymized.
- `asset_id`: turbine ID (anonymized), per-farm numbering.
- `id`: row index within a dataset (0-based), unique per file.
- `train_test`: `train` (history) or `prediction` (tail window containing the event).
- `status_type_id`: operational state (0 Normal, 1 Derated, 2 Idling, 3 Service, 4 Downtime, 5 Other).

## Sensor columns
Pattern: `<sensor_base>_<stat>` where stat in {avg, min, max, std}.
- Farm A: 81 sensor columns; only 3 sensors expose min/max/std; rest avg-only.
  Constant-zero sensors: `sensor_46`, `sensor_49` (placeholder, no unit).
- Farm B: 252 columns (63 sensors x 4 stats).
- Farm C: 952 columns (238 sensors x 4 stats).

## Event metadata (event_info.csv)
- `asset` (A) / `asset_id` (B,C): turbine ID.
- `event_id`: dataset file id.
- `event_label`: `anomaly` or `normal`.
- `event_start`, `event_end`: event interval timestamps.
- `event_start_id`, `event_end_id`: row ids delimiting the interval.
- `event_description`: root cause text (anomaly only).

## Feature metadata (feature_description.csv)
- `sensor_name`, `statistics_type`, `description`, `unit`, `is_angle`, `is_counter`.

## Counts
- 95 datasets, 36 turbines, 3 farms, ~5.24M rows.
- 45 anomaly + 50 normal events.
