from dataclasses import dataclass
from domain.exceptions.base import ApplicationException


@dataclass(frozen=True)
class TextTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Text too long: "{self.text[:255]}..."'
