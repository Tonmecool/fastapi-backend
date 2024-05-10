from datetime import datetime
from uuid import uuid4

import pytest

from domain.entities.messages import (
    Chat,
    Message,
)
from domain.events.messages import NewMessageReceivedEvent
from domain.exceptions.messages import TitleTooLongException
from domain.values.messages import (
    Text,
    Title,
)


def test_create_message_success_short_text():
    text = Text('hello world')
    message = Message(text=text, chat_oid=uuid4())

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_success_long_text():
    text = Text('a' * 1000)
    message = Message(text=text, chat_oid=uuid4())

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title('title')
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        title = Title('a' * 1000)


def test_add_chat_to_message():
    text = Text('hello world')
    message = Message(text=text, chat_oid=uuid4())

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages


def test_new_message_events():
    text = Text('hello world')
    message = Message(text=text, chat_oid=uuid4())

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid
