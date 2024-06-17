from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ListenerAlreadyExistException(ApplicationException):
    listener_oid: str

    @property
    def message(self):
        return f'This Listener already listens: {self.listener_oid}'
