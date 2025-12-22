class GameService:
    def __init__(self, repository):
        self.repository = repository

    def get_daily_mission(self):
        game = self.repository.get()
        return game.get_daily_mission()

    def complete_daily_mission(self):
        game = self.repository.get()
        success = game.complete_daily_mission()
        return game.get_daily_mission(), success