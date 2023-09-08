# tests/test_auth.py

import json
import pytest
from app import create_app, db
from app.models import User, Court, Game
from datetime import datetime, date, time
import warnings
from sqlalchemy.exc import SAWarning
from .common_fixtures import client


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
    
