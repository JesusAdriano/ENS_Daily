from datetime import date
from typing import Any, Dict, Optional

from domain.mission_status import MissionStatus
from domain.reading_text import ReadingText
from utils.date_helpers import deserialize_date, serialize_date


class DailyMission:
    def __init__(self, reading_text: ReadingText) -> None:
        self.reading_text: ReadingText = reading_text
        self.status: MissionStatus = MissionStatus.PENDING
        self.completed_date: Optional[date] = None

    def complete(self) -> None:
        self.status = MissionStatus.COMPLETED
        self.completed_date = date.today()

    def refresh_for_today(self) -> None:
        today = date.today()

        if self.completed_date and self.completed_date < today:
            self.status = MissionStatus.PENDING
            self.completed_date = None

    def to_dict(self, preview: bool = False) -> Dict[str, Any]:
        return {
            "status": str(self.status),
            "completed_date": serialize_date(self.completed_date),
            "text": self.reading_text.to_dict(preview=preview)
        }

    def to_persistence(self) -> Dict[str, Any]:
        return {
            "status": str(self.status),
            "completed_date": serialize_date(self.completed_date),
            "text_id": self.reading_text.id
        }

    @staticmethod
    def from_persistence(data: Dict[str, Any], reading_text: ReadingText) -> "DailyMission":
        mission = DailyMission(reading_text)
        mission.status = MissionStatus(data.get("status", MissionStatus.PENDING))
        mission.completed_date = deserialize_date(data.get("completed_date"))
        return mission

