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
        mission = game.get_daily_mission()
        self.repository.save()
        return mission, success, game.streak

    def get_all_missions(self):
        game = self.repository.get()
        current_mission = game.get_daily_mission()
        all_texts = self.repository.text_repository.get_all()
        
        missions = []
        current_mission_id = None
        
        # Identifica a missão atual (de hoje)
        current_mission_id = current_mission.reading_text.id
        
        for text in all_texts:
            mission_data = {
                "id": text.id,
                "title": text.title,
                "status": "pending"
            }
            
            if text.id in game.completed_mission_ids and text.id != current_mission_id:
                mission_data["status"] = "completed"

            if text.id == current_mission_id:
                mission_data["is_current"] = True
            
            missions.append(mission_data)
        
        return missions, current_mission_id


    def reset_daily_progress(self):
        """Reset para testes - limpa o progresso do dia"""
        game = self.repository.get()
        
        game.daily_mission = None
        game.last_mission_day = None
        game.current_mission_index = 0
        game.completed_mission_ids = []
        game.streak = 0
        game.last_completed_day = None
        
        self.repository.save()
        return True

