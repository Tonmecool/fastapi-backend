from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    title: ClassVar[str] = 'New message received'

    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewChatCreatedEvent(BaseEvent):
    title: ClassVar[str] = 'New chat created'

    chat_oid: str
    chat_title: str


@dataclass
class NewMessageReceivedFromBrokerEvent(BaseEvent):
    event_title: ClassVar[str] = 'New Message From Broker Received'

    message_text: str
    message_oid: str
    chat_oid: str