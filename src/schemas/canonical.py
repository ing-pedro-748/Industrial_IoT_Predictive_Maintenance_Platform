"""Canonical schema definitions for CARE to Compare V6."""
from __future__ import annotations

META_COLUMNS = ["time_stamp", "asset_id", "id", "train_test", "status_type_id"]

# Status type semantics (from README)
STATUS_TYPE_LABELS = {
    0: "Normal Operation",
    1: "Derated Operation",
    2: "Idling",
    3: "Service",
    4: "Downtime",
    5: "Other",
}

NORMAL_STATUS_IDS = {0, 2}

# Column name suffixes used for sensor statistics
STAT_SUFFIXES = ["avg", "min", "max", "std"]

# A canonical sensor is identified by a base name + one or more statistics.
# Farms use different base names; equivalence is established per analysis, not
# assumed. See reports/variable_equivalence.md.
