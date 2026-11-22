-- Snowflake DDL for Industrial IoT Predictive Maintenance Platform
-- Dimension: turbines
CREATE TABLE IF NOT EXISTS DIM_TURBINE (
    turbine_id INT PRIMARY KEY,
    farm VARCHAR(50),
    asset_id INT
);

-- Dimension: date
CREATE TABLE IF NOT EXISTS DIM_DATE (
    date_key DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);

-- Fact: sensor readings (Silver)
CREATE TABLE IF NOT EXISTS FACT_SENSOR_READING (
    reading_id BIGINT AUTOINCREMENT,
    turbine_id INT,
    ts TIMESTAMP,
    status_type_id INT,
    feature_json VARIANT,
    PRIMARY KEY (reading_id)
);

-- Fact: anomaly predictions
CREATE TABLE IF NOT EXISTS FACT_ANOMALY_PREDICTION (
    prediction_id BIGINT AUTOINCREMENT,
    turbine_id INT,
    ts TIMESTAMP,
    anomaly_score FLOAT,
    is_anomaly BOOLEAN,
    model_version VARCHAR(100),
    threshold FLOAT,
    PRIMARY KEY (prediction_id)
);

-- Fact: events
CREATE TABLE IF NOT EXISTS FACT_EVENT (
    event_id INT,
    turbine_id INT,
    event_label VARCHAR(20),
    event_start TIMESTAMP,
    event_end TIMESTAMP,
    event_description VARCHAR(500)
);
"