# tests/common_fixtures.py

import pytest
from app import create_app, db
import json
from app.models import User

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