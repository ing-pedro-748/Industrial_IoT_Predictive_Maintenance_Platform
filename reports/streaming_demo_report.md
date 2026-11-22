# Phase 4 — Streaming Demo Report

## Components implemented
- `src/streaming/simulator.py`: replay historical series as telemetry events with event_time/ingestion_time.
- `src/streaming/consumer.py`: WindowAggregator with sliding windows per turbine.
- `src/streaming/kafka_io.py`: Kafka producer/consumer helpers (requires broker).
- `docker-compose.kafka.yml`: Kafka + Zookeeper for local broker.
- `notebooks/10_streaming_demo.ipynb`: end-to-end demo (no Kafka).

## Demo result
- 500 events published, 6-event sliding window aggregates computed per turbine.

## Next steps
- Run with a real Kafka broker (docker compose -f docker-compose.kafka.yml up).
- Add Spark Structured Streaming consumer.
- Integrate inference service.
- Phase 5: Airflow + Snowflake.
