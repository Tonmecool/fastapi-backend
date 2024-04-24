from dataclasses import dataclass, field
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer
from aiokafka.producer import AIOKafkaProducer
import orjson

from infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    # По хорошему здесь должен быть IProducer
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer
    consumer_map: dict[str, AIOKafkaConsumer] = field(
        default_factory=dict,
        kw_only=True,
    )

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(key=key, topic=topic, value=value)
    
    async def start_consuming(self, topic: str) -> AsyncIterator[tuple[bytes, bytes]]:
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            yield orjson.loads(message.value), message.key.decode()
    
    async def stop_consuming(self):
        self.consumer.unsubscribe()

    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()
    
    async def start(self):
        await self.producer.start()
        await self.consumer.start()
