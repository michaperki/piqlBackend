# tests/test_routes.py

import json
import pytest
from app import create_app, db
from app.models import Item, User, Court, Game
from datetime import datetime, date, time

@pytest.fixture
def client():
    # Create a test Flask app instance
    app = create_app("testing")  # Specify the testing configuration

    # Create a test client to interact with the app
    client = app.test_client()

    # Create a test database for testing
    with app.app_context():
        db.create_all()

    yield client

    # Clean up the test database after testing
    with app.app_context():
        db.drop_all()

def test_register_user(client):
    # Create a test user data
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }

    # Send a POST request to the registration route
    response = client.post('/auth/register', json=user_data)
    data = json.loads(response.data.decode())

    # Check that the response indicates successful registration
    assert response.status_code == 201
    assert data["message"] == "Registration successful"

    # Check that the user is saved in the database
    with client.application.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        assert user is not None
        
def test_login_user(client):
    # Create a test user
    user = User(email="test@example.com", password="testpassword")
    with client.application.app_context():
        db.session.add(user)
        db.session.commit()

    # Create login credentials
    login_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }

    # Send a POST request to the login route
    response = client.post('/auth/login', json=login_data)
    data = json.loads(response.data.decode())

    # Check that the response indicates successful login
    assert response.status_code == 200
    assert "access_token" in data
    
def get_auth_headers(client, email, password):
    # Use a function to retrieve authentication headers for a given user
    # You might need to implement this function based on your token-based authentication system
    # Example: You may need to log in and obtain a token, then use that token for subsequent requests
    # For simplicity, you can pass the token directly in headers here.

    # Replace the following line with your actual authentication mechanism
    token = "your_test_token"

    return {"Authorization": f"Bearer {token}"}

def test_get_courts(client):
    # Create test court data
    court_data = {
        "name": "Test Court",
        "address": "123 Main St",
        "is_public": True,
        "image_url": "test.jpg",
        "number_of_courts": 3,
    }

    # Create a test court in the database
    with client.application.app_context():
        court = Court(**court_data)
        db.session.add(court)
        db.session.commit()

    # Simulate an authenticated request by adding authentication headers
    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")
    response = client.get('/api/courts', headers=auth_headers)  # Include auth headers

    # Check that the response contains court data
    assert response.status_code == 200

    # Parse the JSON response and store it in the 'data' variable
    data = json.loads(response.data.decode())

    assert len(data) == 1  # Assuming one court is created
    assert data[0]["name"] == "Test Court"

def test_get_single_court(client):
    # Create test court data
    court_data = {
        "name": "Test Court",
        "address": "123 Main St",
        "is_public": True,
        "image_url": "test.jpg",
        "number_of_courts": 3,
    }

    # Create a test court in the database
    with client.application.app_context():
        court = Court(**court_data)
        db.session.add(court)
        db.session.commit()

    # Simulate an authenticated request by adding authentication headers
    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")
    response = client.get('/api/courts/1', headers=auth_headers)  # Include auth headers

    # Check that the response contains the court data
    assert response.status_code == 200

    # Parse the JSON response and store it in the 'data' variable
    data = json.loads(response.data.decode())

    assert data["name"] == "Test Court"
    assert data["address"] == "123 Main St"
    
def test_add_court(client):
    # Create a test court data
    court_data = {
        "name": "Test Court",
        "address": "123 Main St",
        "is_public": True,
        "image_url": "test.jpg",
        "number_of_courts": 3,
    }

    # Send a POST request to the courts route
    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")
    response = client.post('/api/courts', json=court_data, headers=auth_headers)

    # Check that the response indicates successful court creation
    assert response.status_code == 200
    assert response.json["message"] == "Court created successfully"

def test_delete_court(client):
    # Create a test court data
    court_data = {
        "name": "Test Court",
        "address": "123 Main St",
        "is_public": True,
        "image_url": "test.jpg",
        "number_of_courts": 3,
    }

    # Create a test court in the database
    with client.application.app_context():
        court = Court(**court_data)
        db.session.add(court)
        db.session.commit()

    # Simulate an authenticated request by adding authentication headers
    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

    # Send a DELETE request to delete the court
    response = client.delete('/api/courts/1', headers=auth_headers)

    # Check that the response indicates successful court deletion
    assert response.status_code == 200
    assert response.json["message"] == "Court deleted successfully"

    # Check that the court is removed from the database
    with client.application.app_context():
        court = db.session.get(Court, 1)  # Use Session.get() instead of Query.get()
        assert court is None

    # Attempt to delete a non-existent court should return a 404 error
    response = client.delete('/api/courts/999', headers=auth_headers)
    assert response.status_code == 404
    assert response.json["error"] == "Court not found"


def test_create_game(client):
    # Convert the date string to a Python date object
    date_str = '2022-12-25'  # Change this to your date string format
    game_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Create test game data
    game_data = {
        "date": game_date.strftime('%Y-%m-%d'),  # Format the date as a string
        "start_time": "10:00:00",  # Convert to string
        "end_time": "12:00:00",    # Convert to string
        "court_id": 1,  # Use an ID for now
        "players": []  # Initialize an empty list
    }

    # Simulate an authenticated request by adding authentication headers
    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

    # Create a test court and users within the same app context
    with client.application.app_context():
        court = Court(name="Test Court", address="123 Main St")
        db.session.add(court)

        user1 = User(email="user1@example.com", password="password1")
        user2 = User(email="user2@example.com", password="password2")
        db.session.add_all([user1, user2])

        db.session.commit()

        # Use the actual Court model instance's ID in game_data
        game_data["court_id"] = court.id

        # Use user IDs in player data
        game_data["players"] = [user1.id, user2.id]  # Use user IDs here

        # Create a new game and add it to the session
        game = Game(
            date=game_date,
            start_time=time(10, 0, 0),
            end_time=time(12, 0, 0),
            court_id=court.id
        )

        # Add players to the game (many-to-many relationship)
        for player_id in game_data["players"]:
            player = User.query.get(player_id)
            if player:
                game.players.append(player)

        db.session.add(game)  # Add the game to the session
        db.session.commit()   # Commit the changes to the database

        # Retrieve the court object within the same session context
        retrieved_court = Court.query.get(court.id)

        # Send a POST request to create a game
        response = client.post('/api/games', json=game_data, headers=auth_headers)

        # Check that the response indicates successful game creation
        assert response.status_code == 201
        assert response.json["message"] == "Game created successfully"

        # Check that the game is saved in the database
        game = Game.query.first()
        assert game is not None
        assert game.date == game_date  # Ensure game.date is a Python date object
        assert game.start_time == time(10, 0, 0)
        assert game.end_time == time(12, 0, 0)
        assert game.court_id == retrieved_court.id  # Use the retrieved Court object's ID
        assert len(game.players) == 2
        assert user1 in game.players
        assert user2 in game.players
