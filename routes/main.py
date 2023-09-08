from flask import Flask, Blueprint, request, jsonify, send_file
from app import db  # Import db directly from app/__init__.py
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return 'Welcome to my Flask app!'

@main_bp.route('/images/<path:filename>')
def serve_image(filename):
    # Construct the path to the image in your static directory
    image_path = os.path.join('static', 'images', filename)
    # Serve the image
    return send_file(image_path)