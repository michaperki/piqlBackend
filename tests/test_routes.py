# tests/test_routes.py

import json
import pytest
from app import create_app, db
from app.models import Item

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
