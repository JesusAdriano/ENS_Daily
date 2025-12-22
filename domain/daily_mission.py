from datetime import date


class DailyMission:
    def __init__(self, reading_text):
        self.reading_text = reading_text
        self.status = "pending"
        self.completed_date = None

    def complete(self):
        self.status = "completed"
        self.completed_date = date.today()

    def refresh_for_today(self):
        today = date.today()

        if self.completed_date and self.completed_date < today:
            self.status = "pending"
            self.completed_date = None

    def to_dict(self, preview: bool = False):
        return {
            "status": self.status,
            "completed_date": (
                self.completed_date.isoformat()
                if self.completed_date else None
            ),
            "text": self.reading_text.to_dict(preview=preview)
        }