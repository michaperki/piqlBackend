from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager  # Import JWTManager

db = SQLAlchemy()
jwt = JWTManager()  # Initialize JWTManager

import os

def create_app(config_name="development"):
    app = Flask(__name__)

    # Load configuration based on the environment
    if config_name == 'testing':
        app.config.from_object('app.config.testing.TestingConfig')
    else:
        app.config.from_object('app.config.development.DevelopmentConfig')

    CORS(app, resources={r"auth/*": {"origins": "http://localhost:3000"}})
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize JWTManager for both main and test configurations
    jwt.init_app(app)
    
    from routes.main import main_bp
    from routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
