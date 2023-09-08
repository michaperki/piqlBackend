from flask import Blueprint, request, jsonify
from app import db
from app.models import User  # Import the User model
from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT-related functions

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/update_username', methods=['POST', 'PUT'])
@jwt_required()  # Require JWT authentication to access this route
def update_username():
    print("update username endpoint hit")
    # Get the user ID from the request (you might use JWT or session for authentication)
    user_id = request.json.get('user_id')  # Adjust this based on your authentication method

    # Find the user by their ID
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Get the new username from the request
    new_username = request.json.get('new_username')

    # Check if the new username is unique (optional, depending on your requirements)
    existing_user_with_username = User.query.filter_by(username=new_username).first()
    if existing_user_with_username:
        return jsonify({'message': 'Username already in use'}), 400

    # Update the user's username
    user.username = new_username

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Username updated successfully'})

@settings_bp.route('/get_username', methods=['GET'])
@jwt_required()  # Require JWT authentication to access this route
def get_username():
    # Get the current user's ID from the JWT token
    current_user_id = get_jwt_identity()

    # Query the current user's username from the database
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Return the username as JSON
    return jsonify({'username': user.username})