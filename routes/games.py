from flask import Blueprint, request, jsonify, g
from app.models import Game, User, Court
from app import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

games_bp = Blueprint('games', __name__)

@games_bp.route('/games', methods=['POST'])
def create_game():
    print("Received a POST request to /api/games")
    data = request.get_json()
    print("Received data:", data)
    # Rest of your route code

    # Extract game information from the request data
    date_str = data.get('date')  # Get date as a string
    start_time_str = data.get('start_time')  # Get start_time as a string
    end_time_str = data.get('end_time')  # Get end_time as a string
    court_id = data.get('court_id')
    player_ids = data.get('players', [])  # List of player IDs

    # Check if the specified court exists
    court = Court.query.get(court_id)
    if not court:
        return jsonify({"error": "Court not found"}), 404

    # Convert the date string to a Python date object
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Convert the start_time and end_time strings to Python time objects
    start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
    end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

    # Create a new game
    game = Game(date=date, start_time=start_time, end_time=end_time, court_id=court_id)

    # Ensure that player_ids is a list, even for a single player
    if not isinstance(player_ids, list):
        player_ids = [player_ids]

    # Add players to the game (many-to-many relationship)
    for player_id in player_ids:
        if player_id:
            # Ensure player_id is an integer
            try:
                player_id = int(player_id)
            except ValueError:
                return jsonify({"error": "Invalid player ID format"}), 400

            # Fetch the User instance associated with player_id
            player = User.query.filter_by(id=player_id).first()
            if player:
                game.players.append(player)
            else:
                return jsonify({"error": "Player not found"}), 404

    # Add the game to the database
    db.session.add(game)
    db.session.commit()

    return jsonify({"message": "Game created successfully"}), 201  # Return a 201 Created status

# Route to join a game by ID
@games_bp.route('/games/<int:game_id>/join', methods=['POST'])
def join_game(game_id):
    data = request.get_json()
    user_id = data.get('user_id')

    # Check if the specified game exists
    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    # Check if the specified user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if the user is already in the game
    if user in game.players:
        return jsonify({"error": "User is already in the game"}), 400

    # Add the user to the game
    game.players.append(user)
    db.session.commit()

    return jsonify({"message": "Joined the game successfully"}), 200

# Route to get all games
@games_bp.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    
    current_user_id = get_jwt_identity()
    print("Current User ID:", current_user_id)
    
    games = Game.query.all()
    game_list = []

    for game in games:
        # Extract player IDs from the User objects in game.players
        player_ids = [player.id for player in game.players]

        game_data = {
            "id": game.id,
            "date": str(game.date),
            "start_time": str(game.start_time),
            "end_time": str(game.end_time),
            "court_id": game.court_id,
            "player_ids": player_ids  # Use the extracted player IDs
        }
        game_list.append(game_data)

    return jsonify(game_list)


# Route to get a single game by ID
@games_bp.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get(game_id)
    if game:
        # Extract player IDs from the User objects in game.players
        player_ids = [player.id for player in game.players]

        game_data = {
            "id": game.id,
            "date": str(game.date),
            "start_time": str(game.start_time),
            "end_time": str(game.end_time),
            "court_id": game.court_id,
            "player_ids": player_ids  # Use the extracted player IDs
        }
        return jsonify(game_data)
    return jsonify({"error": "Game not found"}), 404  # Return a 404 Not Found for missing game