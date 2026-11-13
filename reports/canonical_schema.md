# Canonical Schema

## Principles
- Original data remain immutable in `data/raw/`.
- A canonical schema is defined per farm family first; cross-farm unification
  only for sensors with verified semantic/physical equivalence.
- Sensor base names are not assumed equivalent across farms (e.g. `sensor_0`
  in Farm A vs Farm B may measure different quantities).

## Meta schema (common)
| Column | Type | Required |
|---|---|---|
| time_stamp | datetime | yes |
| asset_id | int | yes |
| id | int | yes |
| train_test | str | yes |
| status_type_id | int | yes |

## Sensor schema (per farm)
- One column per `<base>_<stat>` for available stats.
- Stats subset: {avg} (A partial), {avg,min,max,std} (B,C).
- `asset_id` is constant within a file but varies across files.

## Storage conventions
- Bronze: raw CSV as-is.
- Silver: parsed timestamps, validated schema, typed columns, no imputation.
- Gold: feature-engineered, windowed aggregates, ML-ready (Parquet, partitioned).
