# Initial Dataset Audit — CARE to Compare V6

## 1. Scope and method

This audit was performed by direct inspection of the local archive
`data/raw/care_to_compare/CARE_To_Compare.zip` (5.50 GB, 110 entries) without
extracting it. All facts below were verified by executing code against the
archive. No data was modified, no models were trained, and no values were
imputed or removed.

Companion artifacts:
- `notebooks/01_dataset_exploration.ipynb`
- `reports/dataset_inventory.csv` (file inventory with sizes)

## 2. Verified structural facts

- Archive root folder: `CARE_To_Compare/`.
- 95 dataset CSVs distributed across 3 wind farms:
  - Wind Farm A: 22 datasets
  - Wind Farm B: 15 datasets
  - Wind Farm C: 58 datasets
- Total rows across all dataset CSVs: ~5,242,948.
- Total uncompressed size of dataset CSVs: ~19.99 GB.
- 3 metadata files per farm: `event_info.csv`, `feature_description.csv`.
- `README.md` and `README.txt` are byte-identical (md5 `9a3afda4...`); only
  duplicate content group in the archive.

## 3. Organization by wind farm and turbine

- Wind Farm A: 5 turbines (asset IDs 0, 10, 11, 13, 21), onshore Portugal,
  derived from EDP open data.
- Wind Farm B: 9 turbines (asset IDs 0-14 subset), offshore Germany.
- Wind Farm C: 22 turbines (asset IDs 2-56 subset), offshore Germany.
- Total distinct turbines: 36 (matches documented figure).

## 4. Variables and sensor schemas

Meta columns (present in all farms): `time_stamp`, `asset_id`, `id`,
`train_test`, `status_type_id`.

Sensor column counts (representative files):
- Farm A: 86 columns total (81 sensor columns).
- Farm B: 257 columns total (252 sensor columns).
- Farm C: 957 columns total (952 sensor columns).

Column naming convention observed: `<sensor_name>_<stat>` where stat is one of
`avg`, `min`, `max`, `std`. Not every sensor exposes all four statistics:
- Farm A: only 3 sensors expose min/max/std; the rest are `avg` only. Farm A
  suffix counts: avg 46, max/min/std 9 each (plus 8 single-statistic sensors
  whose names end in numeric ids).
- Farm B and Farm C: every sensor exposes all four statistics.

Feature descriptions (`feature_description.csv`) provide `sensor_name`,
`statistics_type`, `description`, `unit`, `is_angle`, `is_counter`. Statistic
type strings vary in ordering of the words (e.g. "average,maximum,minimum,std_dev"
vs "maximum,minimum,average,std_dev") but describe the same set.

Units differ across farms (e.g. degrees C vs "Celsius"; degrees with various
glyphs; kvarh, kWh, m/s, etc.). `is_angle` and `is_counter` flags are provided.

Some Farm A sensors are constant zero in the representative file
(`sensor_46`, `sensor_49`) with a missing unit in feature_description — likely
unused/placeholder sensors.

## 5. Temporal structure

- Sampling frequency: 10 minutes (median delta verified).
- Timestamps are anonymized strings; parse with `pd.to_datetime`.
- No duplicate timestamps or duplicate row ids within a representative file.
- Series length: ~52,000-66,000 rows per dataset (~1 year per turbine).
- Temporal gaps exist:
  - Farm A: 18 gaps > 10 min in representative file, up to 13 h.
  - Farm B: 1 gap of 20 min.
  - Farm C: 2 gaps of 3 and 5 days.
  These gaps likely correspond to outages/maintenance and must not be silently
  filled.

## 6. Normal vs anomalous periods

- Event metadata (`event_info.csv`) provides per-dataset labels and intervals:
  `event_id`, `event_label` (`anomaly`/`normal`), `event_start`,
  `event_start_id`, `event_end`, `event_end_id`, `event_description`.
  Farm A uses column `asset`; Farms B and C use `asset_id`.
- Verified totals: 45 anomaly + 50 normal = 95 events.
  (README documents 44 anomaly + 51 normal — minor discrepancy; verified counts
  take precedence.)
- Each dataset CSV has a `train_test` column marking `train` (history) vs
  `prediction` (tail window containing the single event).
- Event intervals fall inside the prediction window, with a lead-in of a few
  days, which is relevant for early-detection evaluation.
- `event_start_id`/`event_end_id` map directly to the `id` column of the
  corresponding dataset CSV (verified).

## 7. Data quality findings

- Nulls are sparse: representative files have 0-7 null cells each, in single
  rows (e.g. Farm A `sensor_14_avg`, `sensor_22_avg` on one prediction row;
  Farm B `power_62_max`/`power_62_std` on a few training rows).
- No infinite values in representative files.
- No fully duplicated rows.
- Zeros are frequent and ambiguous: many are legitimate (status 0/4, idling,
  zero power/reactive power) but some sensors are constant zero (likely unused).
  Zeros must not be blindly treated as missing.
- Outliers exist in distributions (e.g. angles -180..180, power 0..max). These
  may be genuine anomalies and must not be removed by statistical rules without
  justification.
- Constant columns: `asset_id` (per file), `sensor_46`, `sensor_49` (Farm A).

## 8. Problems to resolve before processing/training

1. Schema heterogeneity across farms: different sensor sets, different units,
   different statistic availability. Do not concatenate farms without semantic
   equivalence checks.
2. Farm A feature names differ (`wind_speed_3` vs `sensor_*`) and only some
   sensors have min/max/std.
3. Temporal gaps of up to 5 days; need an explicit gap-handling policy.
4. Ambiguous zeros vs missing values.
5. Potential data leakage: `train_test` and event dates must never be used as
   predictive features; splits must be time-based.
6. Labels are interval-based (event windows), not per-row. Need a documented
   rule to associate observations with normal/anomaly periods without inventing
   per-row labels.
7. Anomaly vs failure vs maintenance distinction: `status_type_id` encodes
   operational state (service/downtime) which can leak future information if
   used naively.

## 9. Hypotheses (not yet verified)

- The `prediction` tail window is the evaluation horizon; training portion is
  normal-ish history.
- Gaps correspond to maintenance/outages (status 3/4) rather than random
  missingness.
- Farm A's constant-zero sensors are unused placeholders.

## 10. Still unknown

- Exact row counts and quality metrics for all 95 files (only representative
  files fully profiled; line counts computed for all).
- Cross-file consistency of constant columns and null positions.
- Seasonality and per-turbine drift.
- Whether `id` is contiguous globally or per file (appears per file).

## 11. Recommended next steps (not implemented)

- Build a per-farm schema equivalence table.
- Profile all files for nulls/zeros/constants in a batched, memory-safe way.
- Design time-based train/validation/test splits with gap handling.
- Define the observation-to-event labeling rule for evaluation.
- Only then begin feature engineering and baseline anomaly detection.
