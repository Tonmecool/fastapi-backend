from dataclasses import dataclass

from aiokafka.producer import AIOKafkaProducer

from infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    # По хорошему здесь должен быть IProducer
    producer: AIOKafkaProducer

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(key=key, topic=topic, value=value)
    
    async def consume(self, topic: str):
        ...
