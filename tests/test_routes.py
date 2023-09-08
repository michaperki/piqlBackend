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
    
# Modify the get_auth_headers function to generate the token if needed
def get_auth_headers(client, email, password):
    # Check if the user exists, and if not, create the user.
    with client.application.app_context():
        user = User.query.filter_by(email=email).first()
        if user is None:
            # Create a test user if not already existing
            user_data = {
                "email": email,
                "password": password
            }
            response = client.post('/auth/register', json=user_data)
            assert response.status_code == 201

    # Log in and obtain a token
    login_data = {
        "email": email,
        "password": password
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == 200
    data = json.loads(response.data.decode())

    token = data.get("access_token")

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

# Add this helper function to create a game
def create_test_game(client, court_id, players=[]):
    date_str = '2022-12-25'  # Change this to your date string format
    game_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    game_data = {
        "date": game_date.strftime('%Y-%m-%d'),  # Format the date as a string
        "start_time": "10:00:00",  # Convert to string
        "end_time": "12:00:00",    # Convert to string
        "court_id": court_id,
        "players": players
    }

    auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

    response = client.post('/api/games', json=game_data, headers=auth_headers)

    return response

# Now you can refactor the test_create_game using the helper function
def test_create_game(client):
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

        # Create a game using the court and user IDs
        game_data = {
            "date": "2022-12-25",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "court_id": court.id,
            "players": [user1.id, user2.id]
        }

        # Simulate an authenticated request by adding authentication headers
        auth_headers = get_auth_headers(client, "test@example.com", "testpassword")

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
        assert len(game.players) == 2
        assert user1 in game.players
        assert user2 in game.players