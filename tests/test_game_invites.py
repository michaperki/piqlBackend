# tests/test_game_invites.py
import json
import pytest
from app import create_app, db
from app.models import User, Game
from datetime import datetime, time
from .common_fixtures import client, get_auth_headers

def test_game_invites(client):
    with client.application.app_context():
        # Create test users in the database
        user1 = User(email="user1@example.com", password="password1")
        user2 = User(email="user2@example.com", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Convert time strings to Python time objects
        start_time_str = "10:00:00"
        end_time_str = "12:00:00"
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

        # Convert date string to Python date object
        date_str = "2022-12-25"
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Create a test game invite in the database
        game_invite = Game(date=date, start_time=start_time, end_time=end_time, court_id=1)
        game_invite.invites.append(user1)
        db.session.add(game_invite)
        db.session.commit()

        # Simulate an authenticated request by adding authentication headers for user1
        auth_headers_user1 = get_auth_headers(client, "user1@example.com", "password1")

        # Send a GET request to retrieve game invites for user1
        response = client.get('/api/game-invites', headers=auth_headers_user1)

        # Check that the response contains the game invite
        assert response.status_code == 200

        # Parse the JSON response and store it in the 'data' variable
        data = json.loads(response.data.decode())

        assert len(data) == 1  # Assuming one game invite is created
        assert data[0]["date"] == date_str
        assert data[0]["start_time"] == start_time_str  # You can check the time string here
        assert data[0]["end_time"] == end_time_str  # You can check the time string here
        assert data[0]["court_id"] == 1

        # Check that user2 is not listed as an invitee
        assert user2.id not in [user["id"] for user in data]
        
def test_reject_game_invite(client):
    with client.application.app_context():
        # Create test users in the database
        user1 = User(email="user1@example.com", password="password1")
        user2 = User(email="user2@example.com", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Convert time strings to Python time objects
        start_time_str = "10:00:00"
        end_time_str = "12:00:00"
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

        # Convert date string to Python date object
        date_str = "2022-12-25"
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Create a test game invite in the database
        game_invite = Game(date=date, start_time=start_time, end_time=end_time, court_id=1)
        game_invite.invites.append(user1)
        db.session.add(game_invite)
        db.session.commit()

        # Simulate an authenticated request by adding authentication headers for user1
        auth_headers_user1 = get_auth_headers(client, "user1@example.com", "password1")

        # Send a POST request to reject the game invite
        response = client.post('/api/game-invites/reject/1', headers=auth_headers_user1)

        # Check that the response indicates success
        assert response.status_code == 200

        # Send a GET request to retrieve game invites for user1
        response = client.get('/api/game-invites', headers=auth_headers_user1)

        # Check that the response is empty, indicating that the invite has been rejected
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert len(data) == 0
