"""Kafka producer/consumer helpers (requires a running broker)."""
from __future__ import annotations

from typing import Callable, Dict

try:
    from kafka import KafkaProducer, KafkaConsumer
    KAFKA_AVAILABLE = True
except Exception:
    KAFKA_AVAILABLE = False


def make_producer(bootstrap_servers: str = "localhost:9092"):
    if not KAFKA_AVAILABLE:
        return None
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: __import__("json").dumps(v).encode("utf-8"),
    )


def make_consumer(topic: str, bootstrap_servers: str = "localhost:9092", group_id: str = "pm-consumer"):
    if not KAFKA_AVAILABLE:
        return None
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda v: __import__("json").loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
    )
