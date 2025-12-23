class GameService:
    def __init__(self, repository):
        self.repository = repository

    def get_daily_mission(self):
        game = self.repository.get()
        mission = game.get_daily_mission()
        self.repository.save()
        return mission, game.streak

    def complete_daily_mission(self):
        game = self.repository.get()
        success = game.complete_daily_mission()
        self.repository.save()
        return game.get_daily_mission(), success, game.streak
