# Pilot Variable Sets (Phase 1)

## Sensor equivalence table
- `reports/sensor_equivalence.csv`: 355 sensors across 3 farms with category + unit.
- `reports/pilot_variables.csv`: 173 sensors in categories present in >=2 farms.

## Categories
- temperature (127), current (53), power (37), voltage (28), pressure (24), rotation (18), wind (16), vibration (8), pitch (4), other (40).

## Pilot strategy
For a first anomaly model, prefer sensors available in multiple farms with
compatible units:
- Temperature (deg C / Celsius) — most abundant, directly relevant to failures.
- Power (kW/kvar) — operational load.
- Wind speed (m/s) — driver of expected power.
- Pitch angle (deg) — control variable.

These categories are present in all three farms with compatible units, making
them candidates for cross-farm piloting after unit normalization.

## Not included yet
- Vibration, current, voltage: may be farm-specific; revisit after profiling.
- Counters (is_counter=True in Farm B): treat separately (cumulative).

## Next
- Use profile_all_files.csv (once generated) to confirm constant/missing columns.
- Define the pilot feature set and build a small baseline (Phase 2).
