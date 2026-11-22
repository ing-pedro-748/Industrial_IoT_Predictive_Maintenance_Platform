-- KPI queries for Power BI / analytics

-- Anomalies per turbine (last 30 days)
SELECT turbine_id, COUNT(*) AS n_anomalies
FROM FACT_ANOMALY_PREDICTION
WHERE is_anomaly = TRUE
  AND ts >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY turbine_id
ORDER BY n_anomalies DESC;

-- False alarms per day per turbine (normal events)
-- (requires joining with FACT_EVENT to identify normal periods)

-- Average anomaly score by farm
SELECT t.farm, AVG(p.anomaly_score) AS avg_score
FROM FACT_ANOMALY_PREDICTION p
JOIN DIM_TURBINE t ON p.turbine_id = t.turbine_id
GROUP BY t.farm;
"