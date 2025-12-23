from repository.reading_text_repository import ReadingTextRepository

class ReadingTextService:
    def __init__(self, repository: ReadingTextRepository):
        self.repository = repository

    def get_text_by_id(self, text_id: int):
        return self.repository.get_by_id(text_id)
