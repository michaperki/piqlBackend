from flask import Blueprint, request, jsonify, g
from app.models import User, UserConnection
from app import db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

social_bp = Blueprint('friends', __name__)

@social_bp.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    current_user_id = get_jwt_identity()

    # Query the user_connections table to find the user's friends
    friend_connections = UserConnection.query.filter_by(user_id=current_user_id).all()

    # Extract the connected_user_id from the friend connections
    friend_ids = [connection.connected_user_id for connection in friend_connections]

    # Query the User table to get information about the friends
    friends = User.query.filter(User.id.in_(friend_ids)).all()

    # Return the list of friends as JSON
    friend_list = [{"id": friend.id, "username": friend.username} for friend in friends]
    return jsonify(friend_list)