from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiokafka.consumer import AIOKafkaConsumer


@dataclass
class BaseMessageBroker(ABC):
    # consumer: AIOKafkaConsumer

    # А здесь по хорошему должен быть BaseBroker если вдруг ужалит в жопу почекать Rabbit и можно было гибко свапнуться
    @abstractmethod
    async def send_message(self, topic: str, value: bytes):
        ...

    @abstractmethod
    async def consume(self, topic: str):
        ...
