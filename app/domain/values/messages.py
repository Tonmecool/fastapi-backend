from dataclasses import dataclass

from domain.exceptions.messages import TextTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > 255:
            raise TextTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)