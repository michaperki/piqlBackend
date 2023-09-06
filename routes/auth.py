# routes/auth.py

from flask import Blueprint, request, jsonify
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201
