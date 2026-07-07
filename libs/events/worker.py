import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_EVENTS_TOPIC = os.getenv("KAFKA_EVENTS_TOPIC", "tenant-events")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "notification-worker")


async def run_worker() -> None:
    consumer = AIOKafkaConsumer(
        KAFKA_EVENTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            event = json.loads(message.value.decode())
            event_type = event.get("event_type")
            if event_type != "notification.sent":
                continue
            payload = event.get("payload", {})
            print(
                f"[worker] tenant={payload.get('tenant_id')} "
                f"channel={payload.get('channel')} recipient={payload.get('recipient')}"
            )
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(run_worker())
