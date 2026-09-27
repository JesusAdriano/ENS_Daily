from datetime import date, timedelta
from typing import Any, Dict, Optional

from domain.daily_mission import DailyMission
from domain.reading_text import ReadingText
from utils.date_helpers import deserialize_date, serialize_date


class Game:
    def __init__(self, text_repository: Any, persisted_state: Optional[Dict[str, Any]] = None) -> None:
        self.text_repository = text_repository
        self.daily_mission: Optional[DailyMission] = None
        self.last_mission_day: Optional[date] = None
        self.current_mission_index: int = 0
        self.completed_mission_ids: list[int] = []

        self.streak: int = 0
        self.last_completed_day: Optional[date] = None

        if persisted_state:
            self._load_state(persisted_state)

    def _load_state(self, state: Dict[str, Any]) -> None:
        if state.get("last_mission_day"):
            self.last_mission_day = deserialize_date(state.get("last_mission_day"))

        self.streak = state.get("streak", 0)
        self.last_completed_day = deserialize_date(state.get("last_completed_day"))
        self.completed_mission_ids = state.get("completed_mission_ids", [])

        if "current_mission_index" in state:
            self.current_mission_index = state["current_mission_index"]

        if state.get("daily_mission"):
            text_id = state["daily_mission"].get("text_id")
            text = self.text_repository.get_by_id(text_id)

            if text:
                if "current_mission_index" not in state:
                    self.current_mission_index = max(text.id - 1, 0)
                self.daily_mission = DailyMission.from_persistence(
                    state["daily_mission"], text
                )

    def get_daily_mission(self) -> DailyMission:
        if self.daily_mission is None:
            reading_text: ReadingText = self.text_repository.get_by_index(
                self.current_mission_index
            )
            self.daily_mission = DailyMission(reading_text)
            self.last_mission_day = date.today()

        assert self.daily_mission is not None
        return self.daily_mission

    def complete_daily_mission(self) -> bool:
        mission = self.get_daily_mission()

        if str(mission.status) == "completed":
            return False

        today = date.today()
        yesterday = today - timedelta(days=1)

        if self.last_completed_day == yesterday:
            self.streak += 1
        else:
            self.streak = 1

        self.last_completed_day = today
        mission.complete()
        mission_id = mission.reading_text.id
        if mission_id not in self.completed_mission_ids:
            self.completed_mission_ids.append(mission_id)

        if hasattr(self.text_repository, "get_all"):
            mission_count = len(self.text_repository.get_all())
        else:
            mission_count = len(self.text_repository._texts)
        self.current_mission_index = (self.current_mission_index + 1) % mission_count
        self.daily_mission = None

        return True

    def to_persistence(self) -> Dict[str, Any]:
        return {
            "last_mission_day": serialize_date(self.last_mission_day),
            "streak": self.streak,
            "last_completed_day": serialize_date(self.last_completed_day),
            "current_mission_index": self.current_mission_index,
            "completed_mission_ids": self.completed_mission_ids,
            "daily_mission": (
                self.daily_mission.to_persistence() if self.daily_mission else None
            )
        }

