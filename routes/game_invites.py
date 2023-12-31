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
@game_invites_bp.route('/game-invites/accept/<int:game_id>', methods=['POST'])
@jwt_required()
def accept_game_invite(game_id):
    # Get the current user
    current_user_id = get_jwt_identity()
    if current_user_id is None:
        return jsonify({"msg": "User not found"}), 404
    
    # This line should retrieve the game by its ID, not the current user's ID
    # Replace it with the correct query
    game_invite = Game.query.get(game_id)

    if game_invite is None:
        return jsonify({"msg": "Game invite not found"}), 404

    current_user = User.query.get(current_user_id)

    # Check if the current user is invited to the game
    if current_user not in game_invite.invites:
        return jsonify({"msg": "User is not invited to this game"}), 403

    # Remove the user from the invites list
    game_invite.invites.remove(current_user)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"msg": "Game invite accepted"}), 200

# Route to reject a game invite
@game_invites_bp.route('/game-invites/reject/<int:game_id>', methods=['POST'])
@jwt_required()
def reject_game_invite(game_id):
    current_user_id = get_jwt_identity()

    # There is an issue here; you are using 'invite_id' which is not defined
    # Replace 'invite_id' with 'game_id'
    game_invite = Game.query.filter(Game.invites.any(id=current_user_id), Game.id == game_id).first()

    if not game_invite:
        return jsonify({"error": "Game invite not found or not accessible"}), 404

    # Remove the current user from the game's invites
    user_to_remove = User.query.get(current_user_id)
    game_invite.invites.remove(user_to_remove)
    db.session.commit()

    return jsonify({"message": "Game invite rejected"}), 200