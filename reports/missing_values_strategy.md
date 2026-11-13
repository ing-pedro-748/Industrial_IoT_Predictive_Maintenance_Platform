# Missing Values Strategy

- Nulls are sparse (single cells in representative files).
- Do not impute in Phase 0/1 exploratory work.
- For modeling (Phase 2): evaluate forward-fill within a turbine series
  limited to short gaps, and explicit missing indicators.
- Zeros are NOT treated as missing by default; only sensors flagged as
  constant-zero placeholders (e.g. Farm A `sensor_46`, `sensor_49`) are
  candidates for exclusion.
- Document every imputation decision and its justification.
