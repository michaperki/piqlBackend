from flask import Blueprint, request, jsonify
from app.models import Game, User, Court
from app import db

games_bp = Blueprint('games', __name__)

# Route to create a new game
@games_bp.route('/games', methods=['POST'])
def create_game():
    data = request.get_json()

    # Extract game information from the request data
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    court_id = data.get('court_id')
    player_ids = data.get('player_ids', [])  # List of player IDs

    # Check if the specified court exists
    court = Court.query.get(court_id)
    if not court:
        return jsonify({"error": "Court not found"}), 404

    # Create a new game
    game = Game(date=date, start_time=start_time, end_time=end_time, court_id=court_id)

    # Add players to the game (many-to-many relationship)
    for player_id in player_ids:
        player = User.query.get(player_id)
        if player:
            game.players.append(player)

    # Add the game to the database
    db.session.add(game)
    db.session.commit()

    return jsonify({"message": "Game created successfully"}), 201  # Return a 201 Created status

# Route to get all games
@games_bp.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    game_list = [{
        "id": game.id,
        "date": str(game.date),
        "start_time": str(game.start_time),
        "end_time": str(game.end_time),
        "court_id": game.court_id,
        "players": [{"id": player.id, "email": player.email} for player in game.players]
    } for game in games]

    return jsonify(game_list)

# Route to get a single game by ID
@games_bp.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get(game_id)
    if game:
        game_data = {
            "id": game.id,
            "date": str(game.date),
            "start_time": str(game.start_time),
            "end_time":
