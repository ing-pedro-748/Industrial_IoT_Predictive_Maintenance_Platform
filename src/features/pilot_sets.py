"""Curated pilot feature sets per farm (refined)."""
from __future__ import annotations

PILOT_FEATURES = {
    "A": [
        "sensor_0_avg", "sensor_6_avg", "sensor_11_avg", "sensor_12_avg",
        "sensor_13_avg", "wind_speed_3_avg", "sensor_5_avg", "power_30_avg",
        "power_29_avg", "reactive_power_27_avg",
    ],
    "B": [
        "sensor_8_avg", "sensor_22_avg", "sensor_32_avg", "sensor_34_avg",
        "sensor_38_avg", "sensor_6_avg", "wind_speed_61_avg", "sensor_10_avg",
        "power_62_avg", "power_58_avg",
    ],
    "C": [
        "sensor_7_avg", "sensor_41_avg", "sensor_177_avg", "sensor_178_avg",
        "sensor_186_avg", "sensor_196_avg", "wind_speed_235_avg",
        "wind_speed_237_avg", "power_2_avg", "power_5_avg",
    ],
}
