from flask import Blueprint

# Create a Blueprint object for your routes
main_bp = Blueprint('main', __name__)

# Define a route that responds with "Hello, World!"
@main_bp.route('/')
def hello_world():
    return 'Hello, World!'
