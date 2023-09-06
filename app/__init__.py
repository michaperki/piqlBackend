from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
db = SQLAlchemy()
# app/__init__.py

import os

def create_app():
    app = Flask(__name__)

    # Load configuration based on the environment
    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('app.config.development.DevelopmentConfig')
    else:
        app.config.from_object('app.config.testing.TestingConfig')

    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
