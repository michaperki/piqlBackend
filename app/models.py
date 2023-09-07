from app import db
from bcrypt import hashpw, gensalt, checkpw

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
    password_hash = db.Column(db.String(255), nullable=False)  # Rename 'password' to 'password_hash'

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        # Hash and store the password as a string
        self.password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password):
        # Use bcrypt to check the password
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.email}>'

class HoursOfOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    
class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Optional name field
    address = db.Column(db.String(255), nullable=False)
    is_public = db.Column(db.Boolean, default=True)  # True for public, False for private
    image_url = db.Column(db.String(255))  # You can use this field to store the URL of a court image
    number_of_courts = db.Column(db.Integer, default=1)  # You can set a default value here

    # Define a one-to-many relationship with HoursOfOperation
    hours_of_operation = db.relationship('HoursOfOperation', backref='court', lazy=True)

    def __init__(self, name=None, address=None, is_public=True, image_url=None, number_of_courts=1):
        self.name = name
        self.address = address
        self.is_public = is_public
        self.image_url = image_url
        self.number_of_courts = number_of_courts

    def __repr__(self):
        if self.name:
            return f'<Court {self.name}>'
        else:
            return f'{self.address}>'
        
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'), nullable=False)
    players = db.relationship('User', secondary='game_players', backref='games_played')

    def __init__(self, date, start_time, end_time, court_id):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.court_id = court_id

    def __repr__(self):
        return f'<Game {self.date} - {self.start_time} to {self.end_time}>'

# Define a many-to-many relationship between Game and User for players
game_players = db.Table('game_players',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)