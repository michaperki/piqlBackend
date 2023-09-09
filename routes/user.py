from flask import Blueprint, request, jsonify, g
from app.models import User, UserConnection, FriendRequest
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

@social_bp.route('/friends/send_request', methods=['POST'])
@jwt_required()
def send_friend_request():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    recipient_user_id = data.get('recipient_user_id')

    # Check if the recipient user exists
    recipient_user = User.query.get(recipient_user_id)
    if not recipient_user:
        return jsonify({"message": "Recipient user not found"}), 404

    # Check if the sender is not sending a request to themselves
    if current_user_id == recipient_user_id:
        return jsonify({"message": "Cannot send friend request to yourself"}), 400

    # Check if a friend request already exists
    existing_request = FriendRequest.query.filter_by(sender_id=current_user_id, recipient_id=recipient_user_id).first()
    if existing_request:
        return jsonify({"message": "Friend request already sent"}), 400

    # Create and save the friend request
    friend_request = FriendRequest(sender_id=current_user_id, recipient_id=recipient_user_id)
    db.session.add(friend_request)
    db.session.commit()

    return jsonify({"message": "Friend request sent"}), 200

@social_bp.route('/friends/accept_request/<int:request_id>', methods=['POST'])
@jwt_required()
def accept_friend_request(request_id):
    current_user_id = get_jwt_identity()

    # Check if the friend request exists and is pending
    friend_request = FriendRequest.query.get(request_id)
    if not friend_request or friend_request.recipient_id != current_user_id or friend_request.status != "pending":
        return jsonify({"message": "Friend request not found or not pending"}), 404

    # Update the status of the friend request to "accepted"
    friend_request.status = "accepted"
    db.session.commit()

    # Create a user connection between the sender and recipient
    user_connection1 = UserConnection(user_id=current_user_id, connected_user_id=friend_request.sender_id)
    user_connection2 = UserConnection(user_id=friend_request.sender_id, connected_user_id=current_user_id)
    db.session.add_all([user_connection1, user_connection2])
    db.session.commit()

    return jsonify({"message": "Friend request accepted"}), 200

@social_bp.route('/friends/requests', methods=['GET'])
@jwt_required()
def get_friend_requests():
    current_user_id = get_jwt_identity()

    # Query the friend requests where the current user is the recipient
    friend_requests = FriendRequest.query.filter_by(recipient_id=current_user_id, status="pending").all()

    # Create a list of friend request data
    friend_requests_data = []
    for request in friend_requests:
        friend_requests_data.append({
            "id": request.id,
            "sender_id": request.sender_id,
            "recipient_id": request.recipient_id,
            "status": request.status
        })

    return jsonify(friend_requests_data)