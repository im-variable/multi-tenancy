import json
import os

from aiokafka import AIOKafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_EVENTS_TOPIC = os.getenv("KAFKA_EVENTS_TOPIC", "tenant-events")


async def publish_event(event_type: str, payload: dict) -> None:
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        body = json.dumps({"event_type": event_type, "payload": payload}).encode()
        await producer.send_and_wait(
            KAFKA_EVENTS_TOPIC,
            value=body,
            key=event_type.encode(),
        )
    finally:
        await producer.stop()
