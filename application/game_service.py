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

    def get_all_missions(self):
        game = self.repository.get()
        all_texts = self.repository.text_repository.get_all()
        
        missions = []
        current_mission_id = None
        
        # Identifica a missão atual (de hoje)
        if game.daily_mission:
            current_mission_id = game.daily_mission.reading_text.id
        
        for text in all_texts:
            mission_data = {
                "id": text.id,
                "title": text.title,
                "status": "pending"
            }
            
            # Se é a missão de hoje
            if game.daily_mission and game.daily_mission.reading_text.id == text.id:
                mission_data["status"] = game.daily_mission.status
                mission_data["is_current"] = True
            
            missions.append(mission_data)
        
        return missions, current_mission_id


    def reset_daily_progress(self):
        """Reset para testes - limpa o progresso do dia"""
        game = self.repository.get()
        
        # Reseta o estado diário
        game.daily_mission = None
        game.last_mission_day = None
        
        self.repository.save()
        return True

