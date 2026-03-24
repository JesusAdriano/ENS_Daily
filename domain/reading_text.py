from typing import Dict


class ReadingText:
    def __init__(self, text_id: int, title: str, content: str) -> None:
        if text_id <= 0:
            raise ValueError("text_id deve ser maior que zero")
        if not title.strip():
            raise ValueError("title não pode ser vazio")
        if not content.strip():
            raise ValueError("content não pode ser vazio")

        self.id: int = text_id
        self.title: str = title
        self.content: str = content

    def to_dict(self, preview: bool = False) -> Dict[str, str]:
        if preview:
            return {
                "id": self.id,
                "title": self.title,
                "preview": self.content[:120] + "..."
            }

        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }