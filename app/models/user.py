from app import db
from bcrypt import hashpw, gensalt, checkpw

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(
        db.String(255), nullable=False
    )  # Rename 'password' to 'password_hash'
    username = db.Column(db.String(80), unique=True, nullable=True)  # Add the 'username' field

    def __init__(self, email, password, username=None):  # Update the constructor
        self.email = email
        self.set_password(password)
        self.username = username  # Set the 'username' field

    def set_password(self, password):
        # Hash and store the password as a string
        self.password_hash = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    def check_password(self, password):
        # Use bcrypt to check the password
        return checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,  # Include the 'username' attribute
            # Add other user attributes here if needed
        }

    def __repr__(self):
        return f"<User {self.username}>"
