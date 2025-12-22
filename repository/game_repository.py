from domain.game import Game
from repository.reading_text_repository import ReadingTextRepository


class GameRepository:
    def __init__(self):
        text_repository = ReadingTextRepository()
        self._game = Game(text_repository)

    def get(self) -> Game:
        return self._game