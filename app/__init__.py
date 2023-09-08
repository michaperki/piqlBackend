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

    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize JWTManager for both main and test configurations
    jwt.init_app(app)
    
    from routes import main_bp, auth_bp, courts_bp, games_bp, social_bp, settings_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(courts_bp, url_prefix='/api')
    app.register_blueprint(games_bp, url_prefix='/api')
    app.register_blueprint(social_bp, url_prefix='/api')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')

    return app
