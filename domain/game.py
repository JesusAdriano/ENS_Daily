from datetime import date
from domain.daily_mission import DailyMission

class Game:
    def __init__(self, text_repository):
        self.text_repository = text_repository
        self.daily_mission = None
        self.last_mission_day = None

    def _get_today_index(self):
        """
        Usa o dia do ano como índice.
        Garante que cada dia tenha um texto previsível.
        """
        return date.today().timetuple().tm_yday

    def get_daily_mission(self):
        today = date.today()

        if self.last_mission_day != today:
            text_index = self._get_today_index()
            reading_text = self.text_repository.get_by_index(text_index)

            self.daily_mission = DailyMission(reading_text)
            self.last_mission_day = today

        self.daily_mission.refresh_for_today()
        return self.daily_mission

    def complete_daily_mission(self):
        mission = self.get_daily_mission()

        if mission.status == "completed":
            return False

        mission.complete()
        return True