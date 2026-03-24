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

        # 🔥 STREAK
        self.streak: int = 0
        self.last_completed_day: Optional[date] = None

        if persisted_state:
            self._load_state(persisted_state)

    def _get_today_index(self) -> int:
        return date.today().timetuple().tm_yday

    def _load_state(self, state: Dict[str, Any]) -> None:
        if state.get("last_mission_day"):
            self.last_mission_day = deserialize_date(state.get("last_mission_day"))

        self.streak = state.get("streak", 0)
        self.last_completed_day = deserialize_date(state.get("last_completed_day"))

        if state.get("daily_mission"):
            text_id = state["daily_mission"].get("text_id")
            text = self.text_repository.get_by_id(text_id)

            if text:
                self.daily_mission = DailyMission.from_persistence(
                    state["daily_mission"], text
                )

    def _reset_streak_if_needed(self) -> None:
        if not self.last_completed_day:
            return

        today = date.today()
        yesterday = today - timedelta(days=1)

        if self.last_completed_day < yesterday:
            self.streak = 0

    def get_daily_mission(self) -> DailyMission:
        today = date.today()

        self._reset_streak_if_needed()

        if self.last_mission_day != today or self.daily_mission is None:
            text_index = self._get_today_index()
            reading_text: ReadingText = self.text_repository.get_by_index(text_index)

            self.daily_mission = DailyMission(reading_text)
            self.last_mission_day = today

        assert self.daily_mission is not None
        self.daily_mission.refresh_for_today()
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

        return True

    def to_persistence(self) -> Dict[str, Any]:
        return {
            "last_mission_day": serialize_date(self.last_mission_day),
            "streak": self.streak,
            "last_completed_day": serialize_date(self.last_completed_day),
            "daily_mission": (
                self.daily_mission.to_persistence() if self.daily_mission else None
            )
        }

