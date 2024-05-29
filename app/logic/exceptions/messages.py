from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistException(LogicException):
    title: str

    @property
    def message(self):
        return f'Chat with that title already exist: {self.title}'


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    chat_oid: str

    @property
    def message(self):
        return 'Chat not found'
