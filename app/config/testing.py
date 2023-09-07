# app/config/testing.py

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"  # Use SQLite for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'BRUCE'
    SECRET_KEY = 'BLU'