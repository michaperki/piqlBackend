from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')

    # Initialize the database with the app
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register the Blueprint
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
