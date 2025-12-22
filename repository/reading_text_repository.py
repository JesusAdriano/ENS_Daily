from domain.reading_text import ReadingText

class ReadingTextRepository:
    def __init__(self):
        self._texts = [
            ReadingText(
                1,
                "Foco",
                "Foco é a capacidade de direcionar sua atenção para uma única tarefa..."
            ),
            ReadingText(
                2,
                "Disciplina",
                "Disciplina é fazer o que precisa ser feito mesmo quando não há motivação..."
            ),
            ReadingText(
                3,
                "Consistência",
                "Consistência é o que transforma pequenas ações diárias em grandes resultados..."
            ),
        ]

    def get_by_id(self, text_id: int) -> ReadingText | None:
        for text in self._texts:
            if text.id == text_id:
                return text
        return None

    def get_all(self):
        return self._texts

    def get_by_index(self, index: int) -> ReadingText:
        return self._texts[index % len(self._texts)]