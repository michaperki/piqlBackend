from flask import Blueprint, request, jsonify, g
from app.models import Game, User, Court
from app import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

games_bp = Blueprint('games', __name__)

@games_bp.route('/games', methods=['POST'])
@jwt_required()
def create_game():
    data = request.get_json()
    host_id = get_jwt_identity()

    # Extract game information from the request data
    date_str = data.get('date')
    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    court_id = data.get('court_id')
    player_ids = data.get('players', [])

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

    # Iterate through player_ids to add players to the game
    for player_id in player_ids:
        if player_id:
            try:
                player_id = int(player_id)
            except ValueError:
                return jsonify({"error": "Invalid player ID format"}), 400

            player = User.query.filter_by(id=player_id).first()
            if player:
                if player_id == host_id:
                    # Add host to game.players
                    game.players.append(player)
                else:
                    # Add other players to game.invites
                    game.invites.append(player)
            else:
                return jsonify({"error": "Player not found"}), 404

    # Add the game to the database
    db.session.add(game)
    db.session.commit()

    return jsonify({"message": "Game created successfully"}), 201

@games_bp.route('/games/invite', methods=['POST'])
@jwt_required()
def invite_to_game():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Extract game and player information from the request data
    game_id = data.get('game_id')
    player_id = data.get('player_id')

    # Check if the specified game exists
    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    # Check if the player to be invited exists
    player = User.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    # Check if the player is already invited to the game
    if player in game.invites:
        return jsonify({"error": "Player is already invited to this game"}), 400

    # Add the player to the game invites
    game.invites.append(player)
    db.session.commit()

    return jsonify({"message": "Player invited to the game"}), 201  # Return a 201 Created status

# Route to join a game by ID
@games_bp.route('/games/<int:game_id>/join', methods=['POST'])
@jwt_required()
def join_game(game_id):
    print("Received a POST request to /api/games/<game_id>/join")
    print("game_id:", game_id)
    
    user_id = get_jwt_identity()

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

# Route to get all games with usernames
@games_bp.route('/games', methods=['GET'])
@jwt_required()
def get_games_with_usernames():
    games = Game.query.all()
    game_list = []

    for game in games:
        player_ids = [player.id for player in game.players]

        # Query usernames for the player IDs
        usernames = [User.query.get(player_id).username if User.query.get(player_id) else "(anon)" for player_id in player_ids]
        
        # Query court name for the court ID
        court_name = Court.query.get(game.court_id).name if Court.query.get(game.court_id) else "(private court)"

        game_data = {
            "id": game.id,
            "date": str(game.date),
            "start_time": str(game.start_time),
            "end_time": str(game.end_time),
            "court_id": court_name,  # Use the queried court name
            "usernames": usernames,  # Use the queried usernames
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

@games_bp.route('/games/user', methods=['GET'])
@jwt_required()
def get_user_games():
    user_id = get_jwt_identity()
    
    # Query the games associated with the user
    games = Game.query.filter(Game.players.any(id=user_id)).all()
    
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