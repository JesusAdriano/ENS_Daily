class ReadingText:
    def __init__(self, text_id: int, title: str, content: str):
        self.id = text_id
        self.title = title
        self.content = content

    def to_dict(self, preview: bool = False):
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