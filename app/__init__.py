from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://upsbiqnupwwtng:f1a635fcc73114b225997d2e62eaedf9a59a0eff523909d4af657ab6c04cda89@ec2-44-215-40-87.compute-1.amazonaws.com:5432/d9ees8p5hg2pn7'
    CORS(app)

    # Initialize the database with the app
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register the Blueprint
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
