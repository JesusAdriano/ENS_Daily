from enum import Enum


class MissionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

    def __str__(self) -> str:
        return str(self.value)
