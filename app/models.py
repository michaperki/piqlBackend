from app import db
from bcrypt import hashpw, gensalt

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Item {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = self.hash_password(password)

    def hash_password(self, password):
        salt = gensalt()
        return hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        return hashpw(password.encode('utf-8'), self.password) == self.password

    def __repr__(self):
        return f'<User {self.email}>'