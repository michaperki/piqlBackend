# tests/test_social.py
import json
import pytest
from app import create_app, db
from app.models import User, UserConnection, FriendRequest
from .common_fixtures import client, get_auth_headers

def test_game_invites(client):
    with client.application.app_context():
        # Create test users in the database
        sender_user = User(email="sender@example.com", password="senderpassword")
        recipient_user = User(email="recipient@example.com", password="recipientpassword")
        db.session.add_all([sender_user, recipient_user])
        db.session.commit()

        # Create a new friend request using the sender and recipient users
        friend_request_data = {
            "recipient_user_id": recipient_user.id
        }

        # Simulate an authenticated request by adding authentication headers for the sender user
        auth_headers_sender = get_auth_headers(client, "sender@example.com", "senderpassword")

        # Send a POST request to create a friend request
        response = client.post('/api/friends/send_request', json=friend_request_data, headers=auth_headers_sender)

        # Check that the response indicates a successful friend request creation
        assert response.status_code == 200
        assert response.json["message"] == "Friend request sent"

        # Simulate an authenticated request by adding authentication headers for the recipient user
        auth_headers_recipient = get_auth_headers(client, "recipient@example.com", "recipientpassword")

        # Send a GET request to retrieve friend requests for the recipient user
        response = client.get('/api/friends/requests', headers=auth_headers_recipient)

        # Check that the response contains the friend request
        assert response.status_code == 200

        # Parse the JSON response and store it in the 'data' variable
        data = json.loads(response.data.decode())

        assert len(data) == 1  # Assuming one friend request is created
        assert data[0]["sender_id"] == sender_user.id
        assert data[0]["recipient_id"] == recipient_user.id
        assert data[0]["status"] == "pending"
