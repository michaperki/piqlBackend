# tests/test_social.py
import json
import pytest
from app import create_app, db
from app.models import User, UserConnection, FriendRequest
from .common_fixtures import client, get_auth_headers

# Add a new test function for updating the username
def test_update_username(client):
    with client.application.app_context():
        # Create a test user in the database
        user = User(email="test@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()

        # Define the updated username
        new_username = "new_username"

        # Create a JSON request body with the new username
        update_data = {
            "user_id": user.id,
            "new_username": new_username
        }

        # Simulate an authenticated request by adding authentication headers
        auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

        # Send a POST request to update the username
        response = client.post('/api/settings/update_username', json=update_data, headers=auth_headers)

        # Check that the response indicates successful username update
        assert response.status_code == 200
        assert response.json["message"] == "Username updated successfully"

        # Check that the user's username is updated in the database
        updated_user = User.query.get(user.id)
        assert updated_user.username == new_username


def test_get_username(client):
    with client.application.app_context():
        # Create a test user in the database
        user = User(email="test@example.com", password="testpassword", username="testuser")
        db.session.add(user)
        db.session.commit()

        # Simulate an authenticated request by adding authentication headers
        auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

        # Send a GET request to fetch the current username
        response = client.get('/api/settings/get_username', headers=auth_headers)

        # Check that the response indicates a successful request
        assert response.status_code == 200

        # Parse the JSON response and check the username
        data = response.json
        assert 'username' in data
        assert data['username'] == "testuser"