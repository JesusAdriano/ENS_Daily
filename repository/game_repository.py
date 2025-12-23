import json
from pathlib import Path

from domain.game import Game
from repository.reading_text_repository import ReadingTextRepository

STATE_FILE = Path("game_state.json")
class GameRepository:
    def __init__(self):
        self.text_repository = ReadingTextRepository()
        state = self._load_state()
        self._game = Game(self.text_repository, state)

    def _load_state(self):
        if not STATE_FILE.exists():
            return None

        with STATE_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_state(self):
        with STATE_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                self._game.to_persistence(),
                file,
                ensure_ascii=False,
                indent=2
            )

    def get(self) -> Game:
        return self._game

    def save(self):
        self._save_state()
