from datetime import date, timedelta
from domain.daily_mission import DailyMission
class Game:
    def __init__(self, text_repository, persisted_state=None):
        self.text_repository = text_repository
        self.daily_mission = None
        self.last_mission_day = None

        # 🔥 STREAK
        self.streak = 0
        self.last_completed_day = None

        if persisted_state:
            self._load_state(persisted_state)

    def _get_today_index(self):
        return date.today().timetuple().tm_yday

    def _load_state(self, state):
        if state.get("last_mission_day"):
            self.last_mission_day = date.fromisoformat(
                state["last_mission_day"]
            )

        self.streak = state.get("streak", 0)

        if state.get("last_completed_day"):
            self.last_completed_day = date.fromisoformat(
                state["last_completed_day"]
            )

        if state.get("daily_mission"):
            text = self.text_repository.get_by_id(
                state["daily_mission"]["text_id"]
            )

            if text:
                self.daily_mission = DailyMission.from_persistence(
                    state["daily_mission"], text
                )

    def _reset_streak_if_needed(self):
        if not self.last_completed_day:
            return

        today = date.today()
        yesterday = today - timedelta(days=1)

        if self.last_completed_day < yesterday:
            self.streak = 0

    def get_daily_mission(self):
        today = date.today()

        self._reset_streak_if_needed()

        if self.last_mission_day != today:
            text_index = self._get_today_index()
            reading_text = self.text_repository.get_by_index(text_index)

            self.daily_mission = DailyMission(reading_text)
            self.last_mission_day = today

        self.daily_mission.refresh_for_today()
        return self.daily_mission

    def complete_daily_mission(self):
        mission = self.get_daily_mission()

        # já completou hoje
        if mission.status == "completed":
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

    def to_persistence(self):
        return {
            "last_mission_day": (
                self.last_mission_day.isoformat()
                if self.last_mission_day else None
            ),
            "streak": self.streak,
            "last_completed_day": (
                self.last_completed_day.isoformat()
                if self.last_completed_day else None
            ),
            "daily_mission": (
                self.daily_mission.to_persistence()
                if self.daily_mission else None
            )
        }
