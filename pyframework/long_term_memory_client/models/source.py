from enum import Enum


class Source(str, Enum):
    CHAT = "chat"
    EMAIL = "email"
    FILE = "file"

    def __str__(self) -> str:
        return str(self.value)
