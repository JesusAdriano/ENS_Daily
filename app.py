from flask import Flask, jsonify

from repository.game_repository import GameRepository
from application.game_service import GameService

app = Flask(__name__)

repository = GameRepository()
service = GameService(repository)

@app.route('/api/mission/daily', methods=['GET'])
def get_daily_mission():
    mission = service.get_daily_mission()
    return jsonify(mission.to_dict(preview=True)), 200

@app.route('/api/mission/daily/complete', methods=['GET'])
def complete_daily_mission():
    mission, success = service.complete_daily_mission()

    return jsonify({
        "success": success,
        "mission": mission.to_dict()
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)