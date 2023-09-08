# routes/__init__.py

from flask import Blueprint

# Import your Blueprint modules here
from .main import main_bp
from .auth import auth_bp
from .courts import courts_bp
from .games import games_bp
from .social import social_bp
from .settings import settings_bp
