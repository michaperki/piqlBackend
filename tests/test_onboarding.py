# tests/test_social.py
import json
import pytest
from app import create_app, db
from app.models import User, UserConnection, FriendRequest
from .common_fixtures import client, get_auth_headers
from sqlalchemy.orm import relationship
        
# Add a new test function for fetching onboarding status
def test_get_onboarding_status(client):
    with client.application.app_context():
        # Create a test user in the database
        user = User(email="test@example.com", password="testpassword", onboarded=False)
        db.session.add(user)
        db.session.commit()

        # Simulate an authenticated request by adding authentication headers
        auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

        # Send a GET request to fetch the onboarding status
        response = client.get('/api/settings/onboarding-status', headers=auth_headers)

        # Check that the response indicates a successful request
        assert response.status_code == 200

        # Parse the JSON response and check the onboarding status
        data = response.json
        assert 'onboarded' in data
        assert data['onboarded'] is False


# Add a new test function for completing onboarding
def test_complete_onboarding(client):
    with client.application.app_context():
        # Create a test user in the database
        user = User(email="test@example.com", password="testpassword", onboarded=False)
        db.session.add(user)
        db.session.commit()

        # Simulate an authenticated request by adding authentication headers
        auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

        # Send a POST request to complete onboarding
        response = client.post('/api/settings/complete-onboarding', headers=auth_headers)

        # Check that the response indicates successful onboarding completion
        assert response.status_code == 200
        assert response.json["message"] == "Onboarding completed successfully"

        # Check that the user's onboarded status is updated in the database
        updated_user = User.query.get(user.id)
        assert updated_user.onboarded is True