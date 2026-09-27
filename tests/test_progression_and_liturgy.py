from domain.game import Game
from domain.reading_text import ReadingText
from application.game_service import GameService
from repository.reading_text_repository import ReadingTextRepository


class TextRepository:
    def __init__(self):
        self._texts = [
            ReadingText(1, "Um", "Texto um"),
            ReadingText(2, "Dois", "Texto dois"),
            ReadingText(3, "Tres", "Texto tres"),
            ReadingText(4, "Quatro", "Texto quatro"),
        ]

    def get_by_id(self, text_id):
        return next((text for text in self._texts if text.id == text_id), None)

    def get_by_index(self, index):
        return self._texts[index % len(self._texts)]

    def get_all(self):
        return self._texts


class GameRepository:
    def __init__(self, game):
        self.game = game
        self.text_repository = game.text_repository

    def get(self):
        return self.game

    def save(self):
        pass


def test_missions_cycle_back_to_first_after_fourth():
    game = Game(TextRepository())
    mission_ids = []

    for _ in range(5):
        mission_ids.append(game.get_daily_mission().reading_text.id)
        assert game.complete_daily_mission() is True

    assert mission_ids == [1, 2, 3, 4, 1]


def test_reset_returns_to_first_mission_and_clears_streak():
    game = Game(TextRepository())
    game.complete_daily_mission()
    game.complete_daily_mission()

    GameService(GameRepository(game)).reset_daily_progress()

    assert game.get_daily_mission().reading_text.id == 1
    assert game.streak == 0
    assert game.last_completed_day is None
    assert game.completed_mission_ids == []


def test_current_mission_index_is_persisted():
    repository = TextRepository()
    game = Game(repository)
    game.complete_daily_mission()

    restored = Game(repository, game.to_persistence())

    assert restored.get_daily_mission().reading_text.id == 2


def test_liturgy_evangelho_is_formatted():
    class Liturgy:
        def get_today(self):
            return {
                "data": "27/09/2026",
                "liturgia": "26º Domingo do Tempo Comum",
                "referencia": "Mt 21,28-32",
                "titulo": "Proclamação do Evangelho",
                "texto": "Texto do Evangelho.",
            }

    text = ReadingTextRepository(Liturgy()).get_by_id(4)

    assert text.title == "Proclamação do Evangelho (Mt 21,28-32)"
    assert "Data: 27/09/2026" in text.content
    assert "Liturgia: 26º Domingo do Tempo Comum" in text.content
    assert "Texto do Evangelho." in text.content


def test_liturgy_failure_uses_local_fallback():
    class UnavailableLiturgy:
        def get_today(self):
            return None

    text = ReadingTextRepository(UnavailableLiturgy()).get_by_id(4)

    assert text.title == "Escuta da Palavra"
    assert text.content == "Leitura da Palavra..."
