from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey("court.id"), nullable=False)
    players = db.relationship("User", secondary="game_players", backref="games_played")

    def __init__(self, date, start_time, end_time, court_id):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.court_id = court_id

    def __repr__(self):
        return f"<Game {self.date} - {self.start_time} to {self.end_time}>"


# Define a many-to-many relationship between Game and User for players
game_players = db.Table(
    "game_players",
    db.Column("game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)
