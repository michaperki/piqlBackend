# game_invites.py

from flask import Blueprint, request, jsonify
from app.models import Game, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

game_invites_bp = Blueprint('game_invites', __name__)

# Route to fetch game invites for the current user
@game_invites_bp.route('/game-invites', methods=['GET'])
@jwt_required()
def get_game_invites():
    current_user_id = get_jwt_identity()

    # Query the game_invites table to find invites for the current user
    game_invites = Game.query.filter(Game.invites.any(id=current_user_id)).all()

    # Convert game invite data to a list of dictionaries
    game_invites_data = []
    for game_invite in game_invites:
        game_data = {
            "id": game_invite.id,
            "date": str(game_invite.date),
            "start_time": str(game_invite.start_time),
            "end_time": str(game_invite.end_time),
            "court_id": game_invite.court_id,
            # You can include additional game invite information here
        }
        game_invites_data.append(game_data)

    return jsonify(game_invites_data)

# Route to accept a game invite
@game_invites_bp.route('/game-invites/accept/<int:invite_id>', methods=['POST'])
@jwt_required()
def accept_game_invite(invite_id):
    current_user_id = get_jwt_identity()

    # Query the game_invites table to find the game invite by ID
    game_invite = Game.query.filter(Game.invites.any(id=current_user_id), Game.id == invite_id).first()

    if not game_invite:
        return jsonify({"error": "Game invite not found or not accessible"}), 404

    # Add the current user to the game's players
    game_invite.players.append(current_user_id)
    db.session.commit()

    return jsonify({"message": "Game invite accepted"}), 200

# Add more routes for game invites as needed

# ...
