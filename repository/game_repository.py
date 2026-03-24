import json
from pathlib import Path
from typing import Optional

from domain.game import Game
from repository.reading_text_repository import ReadingTextRepository


class GameRepository:
    def __init__(
        self,
        text_repository: Optional[ReadingTextRepository] = None,
        state_file: Optional[Path] = None,
    ) -> None:
        self.text_repository = text_repository or ReadingTextRepository()
        self.state_file = state_file or Path("game_state.json")

        state = self._load_state()
        self._game = Game(self.text_repository, state)

    def _load_state(self) -> Optional[dict]:
        if not self.state_file.exists():
            return None

        with self.state_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_state(self) -> None:
        with self.state_file.open("w", encoding="utf-8") as file:
            json.dump(
                self._game.to_persistence(),
                file,
                ensure_ascii=False,
                indent=2,
            )

    def get(self) -> Game:
        return self._game

    def save(self) -> None:
        self._save_state()
