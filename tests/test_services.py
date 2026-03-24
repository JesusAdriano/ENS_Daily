import pytest
from datetime import date, timedelta

from domain.game import Game
from domain.daily_mission import DailyMission
from domain.reading_text import ReadingText
from domain.mission_status import MissionStatus


class DummyTextRepo:
    def __init__(self):
        self._texts = [ReadingText(1, "Teste", "Conteúdo")]  # válido

    def get_by_id(self, text_id: int):
        return next((x for x in self._texts if x.id == text_id), None)

    def get_by_index(self, index: int):
        return self._texts[index % len(self._texts)]


def test_mission_status_enum():
    assert MissionStatus.PENDING.value == "pending"
    assert str(MissionStatus.COMPLETED) == "completed"


def test_reading_text_validation():
    with pytest.raises(ValueError):
        ReadingText(0, "Titulo", "Conteúdo")

    with pytest.raises(ValueError):
        ReadingText(1, "", "Conteúdo")

    with pytest.raises(ValueError):
        ReadingText(1, "Titulo", "")

    text = ReadingText(1, "Titulo", "abc")
    assert text.to_dict(preview=True)["preview"] == "abc..."
    assert text.to_dict()["content"] == "abc"


def test_daily_mission_lifecycle():
    text = ReadingText(1, "Titulo", "Texto completo")
    mission = DailyMission(text)

    assert mission.status == MissionStatus.PENDING
    assert mission.completed_date is None

    mission.complete()
    assert mission.status == MissionStatus.COMPLETED
    assert mission.completed_date == date.today()

    mission.refresh_for_today()
    assert mission.status == MissionStatus.COMPLETED

    mission.completed_date = date.today() - timedelta(days=2)
    mission.refresh_for_today()
    assert mission.status == MissionStatus.PENDING

    persistence = mission.to_persistence()
    loaded = DailyMission.from_persistence(persistence, text)
    assert loaded.status == MissionStatus.PENDING
    assert loaded.completed_date is None


def test_game_streak_logic():
    repo = DummyTextRepo()
    game = Game(repo)

    mission = game.get_daily_mission()
    assert isinstance(mission, DailyMission)

    # complete first time
    assert game.complete_daily_mission() is True
    assert game.streak == 1

    # complete again same day should not increase
    assert game.complete_daily_mission() is False
    assert game.streak == 1

    # simulate yesterday completed -> streak increments
    game.last_completed_day = date.today() - timedelta(days=1)
    game.daily_mission = None
    assert game.complete_daily_mission() is True
    assert game.streak == 2

    # simulate break in streak
    game.last_completed_day = date.today() - timedelta(days=2)
    game.daily_mission = None
    assert game.complete_daily_mission() is True
    assert game.streak == 1
