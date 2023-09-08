# tests/test_social.py
import json
import pytest
from app import create_app, db
from app.models import User, UserConnection
from .common_fixtures import client, get_auth_headers

def test_get_friends(client):
    # Create test users in the database
    with client.application.app_context():
        user1 = User(email="user1@example.com", password="password1")
        user2 = User(email="user2@example.com", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Create a user connection between user1 and user2
        user_connection = UserConnection(user_id=user1.id, connected_user_id=user2.id)
        db.session.add(user_connection)
        db.session.commit()

        # Query the database for user2 within the same context
        user2 = User.query.filter_by(email="user2@example.com").first()

    # Authenticate as user1
    auth_headers = get_auth_headers(client, "user1@example.com", "password1")

    # Send a GET request to the social route to get user1's friends
    response = client.get('/api/friends', headers=auth_headers)

    # Check that the response contains user2 as a friend
    assert response.status_code == 200

    # Parse the JSON response and store it in the 'data' variable
    data = json.loads(response.data.decode())

    assert len(data) == 1  # Assuming only one friend is connected
    assert data[0]["id"] == user2.id
