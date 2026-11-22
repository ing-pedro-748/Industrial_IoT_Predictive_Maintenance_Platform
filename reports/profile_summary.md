# Batch Profile Summary (95 datasets)

## Coverage
- 95/95 dataset files profiled.
- Total rows: ~5,242,948 (A 1,196,747; B 859,065; C 3,187,136).

## Nulls
- Total null cells: 175,816.
- Files with nulls: 28.
- Farm C dominates (175,684), largely from dataset 36 (175,684 nulls across 836 columns, 432 rows each — a contiguous missing block).
- Farms A/B have sparse single-cell nulls (40 and 92 total).

## Temporal gaps
- Farm A: 460 gaps across 22 files (max 13,730 min ≈ 9.5 days).
- Farm B: 87 gaps across 15 files (max 3,110 min ≈ 2.2 days).
- Farm C: 40 gaps across 58 files (max 14,410 min ≈ 10 days).

## Implications
- Farm C dataset 36 needs special handling (large contiguous missing block).
- Gap handling must be explicit and per-file; some gaps are multi-day.
- Null imputation strategy should account for contiguous blocks, not just
  single missing cells.
- Per-column null rates should be computed before selecting pilot sensors.
