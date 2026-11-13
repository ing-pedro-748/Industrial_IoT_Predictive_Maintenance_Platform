# Variable Equivalence Analysis (Phase 1 preliminary)

## Meta columns
Identical names across farms: `time_stamp`, `asset_id`, `id`, `train_test`,
`status_type_id`.

## Sensor columns
- Farm A bases: 47 unique bases, mostly `sensor_*`, plus `wind_speed_3/4`.
- Farm B bases: 63 (`sensor_*`, `power_*`, `reactive_power_*`).
- Farm C bases: 238 (`sensor_*`, `power_*`, plus named components).

## Conclusion
Sensor base names are **not** directly comparable across farms. Equivalence
must be established via `feature_description.csv` (description + unit + angle/counter
flags) and physical reasoning, not by name. A per-sensor mapping table will be
built in a later step before any cross-farm combination.
