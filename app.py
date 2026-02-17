from flask import Flask, jsonify, render_template, send_from_directory
from pathlib import Path

from repository.game_repository import GameRepository
from repository.reading_text_repository import ReadingTextRepository
from application.game_service import GameService
from application.reading_text_service import ReadingTextService

app = Flask(__name__, static_folder='static', static_url_path='/static')

game_repository = GameRepository()
text_repository = ReadingTextRepository()

game_service = GameService(game_repository)
text_service = ReadingTextService(text_repository)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/static/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js', mimetype='application/javascript')

@app.route('/static/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

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

@app.route('/api/missions', methods=['GET'])
def get_all_missions():
    missions, current_mission_id = game_service.get_all_missions()
    
    return jsonify({
        "missions": missions,
        "current_mission_id": current_mission_id
    }), 200

@app.route('/api/reset', methods=['POST'])
def reset_daily_progress():
    """ENDPOINT DE TESTES - Reseta o progresso do dia"""
    game_service.reset_daily_progress()
    return jsonify({"success": True, "message": "Progresso resetado para testes"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
