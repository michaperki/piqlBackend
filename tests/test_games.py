# tests/test_routes.py

import json
import pytest
from app import create_app, db
from app.models import User, Court, Game
from datetime import datetime, date, time
import warnings
from sqlalchemy.exc import SAWarning
from .common_fixtures import client, get_auth_headers
from flask_jwt_extended import create_access_token
    
# Add this helper function to create a game
def create_test_game(client, court_id, players=[]):
    date_str = '2022-12-25'  # Change this to your date string format
    game_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    game_data = {
        "date": game_date.strftime('%Y-%m-%d'),  # Format the date as a string
        "start_time": "10:00:00",  # Convert to string
        "end_time": "12:00:00",    # Convert to string
        "court_id": court_id,
        "players": players,
    }

    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

    response = client.post('/api/games', json=game_data, headers=auth_headers)

    return response

def test_create_game(client):
    with client.application.app_context():
        # Create test users in the database
        user1 = User(email="user1@example.com", password="password1")
        db.session.add(user1)
        db.session.commit()

        # Create a test court in the database
        court = Court(name="Test Court", address="123 Main St")
        db.session.add(court)
        db.session.commit()

        # Create an access token for the test user
        access_token = create_access_token(identity=user1.id)

        # Create a game using the court and user ID
        game_data = {
            "date": "2022-12-25",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "court_id": court.id,
            "players": [user1.id],
        }

        # Include the access token in the authentication headers
        auth_headers = {"Authorization": f"Bearer {access_token}"}

        # Send a POST request to create a game
        response = client.post('/api/games', json=game_data, headers=auth_headers)

        # Check that the response indicates successful game creation
        assert response.status_code == 201
        assert response.json["message"] == "Game created successfully"

        # Check that the game is saved in the database
        game = Game.query.first()
        assert game is not None
        assert game.date == date(2022, 12, 25)
        assert game.start_time == time(10, 0, 0)
        assert game.end_time == time(12, 0, 0)
        assert game.court_id == court.id
        assert len(game.players) == 1
        assert user1 in game.players

def test_invite_to_game(client):
    with client.application.app_context():
        # Create test users in the database
        host_user = User(email="host@example.com", password="hostpassword")
        player_user = User(email="player@example.com", password="playerpassword")
        db.session.add_all([host_user, player_user])
        db.session.commit()

        # Create a test court in the database
        court = Court(name="Test Court", address="123 Main St")
        db.session.add(court)
        db.session.commit()

        # Create a game using the court and host_user
        game_data = {
            "date": "2022-12-25",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "court_id": court.id,
            "players": [host_user.id],
        }

        # Suppress SAWarnings
        warnings.filterwarnings("ignore", category=SAWarning)

        # Simulate an authenticated request by adding authentication headers for host_user
        auth_headers_host = get_auth_headers(client, "host@example.com", "hostpassword")

        # Send a POST request to create a game
        response = client.post('/api/games', json=game_data, headers=auth_headers_host)

        # Check that the response indicates successful game creation
        assert response.status_code == 201

        # Fetch the created game from the database
        game = Game.query.first()

        # Invite player_user to the game
        invite_data = {
            "game_id": game.id,
            "player_id": player_user.id
        }

        # Simulate an authenticated request by adding authentication headers for host_user
        auth_headers_host = get_auth_headers(client, "host@example.com", "hostpassword")

        # Send a POST request to invite player_user to the game
        response = client.post('/api/games/invite', json=invite_data, headers=auth_headers_host)

        # Check that the response indicates successful game invitation
        assert response.status_code == 201
        assert response.json["message"] == "Player invited to the game"

        # Check that player_user is in the game's invites list
        game = Game.query.first()
        assert game is not None
        assert len(game.invites) == 1
        assert player_user in game.invites


# Add a new test function for joining a game
def test_join_game(client):
    with client.application.app_context():
        # Create test users in the database
        user1 = User(email="user1@example.com", password="password1")
        user2 = User(email="user2@example.com", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Create a test court in the database
        court = Court(name="Test Court", address="123 Main St")
        db.session.add(court)
        db.session.commit()

        # Create a game using the court and user1
        game_data = {
            "date": "2022-12-25",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "court_id": court.id,
            "players": [user1.id]
        }

        # Suppress SAWarnings
        warnings.filterwarnings("ignore", category=SAWarning)

        # Simulate an authenticated request by adding authentication headers for user1
        auth_headers_user1 = get_auth_headers(client, "user1@example.com", "password1")

        # Send a POST request to create a game
        response = client.post('/api/games', json=game_data, headers=auth_headers_user1)

        # Check that the response indicates successful game creation
        assert response.status_code == 201
        assert response.json["message"] == "Game created successfully"

        # Fetch the created game from the database
        game = Game.query.first()

        # Join the game using user2
        join_data = {
            "user_id": user2.id
        }

        # Simulate an authenticated request by adding authentication headers for user2
        auth_headers_user2 = get_auth_headers(client, "user2@example.com", "password2")

        # Send a POST request to join the game using the fetched game ID
        response = client.post(f'/api/games/{game.id}/join', json=join_data, headers=auth_headers_user2)

        # Check that the response indicates successful game join
        assert response.status_code == 200
        assert response.json["message"] == "Joined the game successfully"

        # Check that user2 is in the game's player list
        game = Game.query.first()
        assert game is not None
        assert len(game.players) == 2
        assert user1 in game.players
        assert user2 in game.players
        
def test_get_games(client):
    # Create test games in the database
    with client.application.app_context():
        game1 = Game(date=date(2023, 9, 1), start_time=time(10, 0, 0), end_time=time(12, 0, 0), court_id=1)
        game2 = Game(date=date(2023, 9, 2), start_time=time(14, 0, 0), end_time=time(16, 0, 0), court_id=2)
        db.session.add_all([game1, game2])
        db.session.commit()

    # Simulate an authenticated request by adding authentication headers
    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

    # Send a GET request to retrieve all games
    response = client.get('/api/games', headers=auth_headers)

    # Check that the response contains game data
    assert response.status_code == 200

    # Parse the JSON response and store it in the 'data' variable
    data = json.loads(response.data.decode())

    assert len(data) == 2  # Assuming two games are created
    assert data[0]["date"] == "2023-09-01"
    assert data[1]["date"] == "2023-09-02"

def test_get_game(client):
    # Create a test game in the database
    with client.application.app_context():
        game = Game(date=date(2023, 9, 1), start_time=time(10, 0, 0), end_time=time(12, 0, 0), court_id=1)
        db.session.add(game)
        db.session.commit()

    # Simulate an authenticated request by adding authentication headers
    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

    # Send a GET request to retrieve the game by its ID (assuming game ID is 1)
    response = client.get('/api/games/1', headers=auth_headers)

    # Check that the response contains the game data
    assert response.status_code == 200

    # Parse the JSON response and store it in the 'data' variable
    data = json.loads(response.data.decode())

    assert data["date"] == "2023-09-01"
    assert data["start_time"] == "10:00:00"

def test_get_games_without_token(client):
    # Send a GET request to the protected route without a valid token
    response = client.get('/api/games')
    
    # Check that the response indicates an unauthorized access (401)
    assert response.status_code == 401
    
def test_get_user_games(client):
    # Create test users in the database
    with client.application.app_context():
        user1 = User(email="test1@gmail.com", password="password1")
        user2 = User(email="test2@gmail.com", password="password2")
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Create test games in the database
        game1 = Game(date=date(2023, 9, 1), start_time=time(10, 0, 0), end_time=time(12, 0, 0), court_id=1) 
        game2 = Game(date=date(2023, 9, 2), start_time=time(14, 0, 0), end_time=time(16, 0, 0), court_id=2)
        game1.players.append(user1)
        game2.players.append(user2)
        db.session.add_all([game1, game2])
        db.session.commit()
        
        # Simulate an authenticated request by adding authentication headers for user1
        auth_headers_user1 = get_auth_headers(client, "test1@gmail.com", "password1")
        
        # Send a GET request to retrieve all games for user1
        response = client.get('/api/games/user', headers=auth_headers_user1)
        
        # Check that the response contains game data
        assert response.status_code == 200
        
        # Parse the JSON response and store it in the 'data' variable
        data = json.loads(response.data.decode())
        
        assert len(data) == 1  # Assuming one game is created
        assert data[0]["date"] == "2023-09-01"
        assert data[0]["start_time"] == "10:00:00"
        
        # Check that user2 is not listed as a player
        assert user2.id not in [user["id"] for user in data]
        
        