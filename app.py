from flask import Flask, jsonify, render_template

from repository.game_repository import GameRepository
from repository.reading_text_repository import ReadingTextRepository
from application.game_service import GameService
from application.reading_text_service import ReadingTextService

app = Flask(__name__)

game_repository = GameRepository()
text_repository = ReadingTextRepository()

game_service = GameService(game_repository)
text_service = ReadingTextService(text_repository)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/mission/daily', methods=['GET'])
def get_daily_mission():
    mission, streak = game_service.get_daily_mission()

    return jsonify({
        "streak": streak,
        "mission": mission.to_dict(preview=True)
    }), 200

@app.route('/api/text/<int:text_id>', methods=['GET'])
def get_text(text_id):
    text = text_service.get_text_by_id(text_id)

    if not text:
        return jsonify({"error": "Text not found"}), 404

    return jsonify(text.to_dict()), 200

@app.route('/api/mission/daily/complete', methods=['GET'])
def complete_daily_mission():
    mission, success, streak = game_service.complete_daily_mission()

    return jsonify({
        "success": success,
        "streak": streak,
        "mission": mission.to_dict(preview=True)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
