from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///piql.db'  # SQLite database file

    # Initialize the database with the app
    db.init_app(app)

    # Register the Blueprint
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
