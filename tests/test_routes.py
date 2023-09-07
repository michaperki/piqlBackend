# tests/test_routes.py

import json
import pytest
from app import create_app, db
from app.models import Item, User

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

def test_get_items(client):
    # Add a test item to the database
    item = Item(name="Test Item")
    with client.application.app_context():
        db.session.add(item)
        db.session.commit()

    # Send a GET request to the `/` route
    response = client.get('/')
    data = json.loads(response.data.decode())

    # Check that the response contains the added item
    assert response.status_code == 200
    assert len(data) == 1  # Assuming it's a list of items
    assert data[0]['name'] == "Test Item"

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