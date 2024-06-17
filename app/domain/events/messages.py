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
class ChatDeletedEvent(BaseEvent):
    title: ClassVar[str] = 'Chat has been deleted'

    chat_oid: str


@dataclass
class ListenerAddedEvent(BaseEvent):
    event_title: ClassVar[str] = 'New listener added'

    listener_oid: str
