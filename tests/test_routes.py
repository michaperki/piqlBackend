# tests/test_routes.py

import json
import pytest
from app import create_app, db
from app.models import Item, User, Court

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
    