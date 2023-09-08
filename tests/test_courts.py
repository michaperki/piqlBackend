# tests/test_routes.py

import json
import pytest
from app import create_app, db
from app.models import User, Court, Game
from datetime import datetime, date, time
import warnings
from sqlalchemy.exc import SAWarning
from .common_fixtures import client, get_auth_headers

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