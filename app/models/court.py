from app import db

class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Optional name field
    address = db.Column(db.String(255), nullable=False)
    is_public = db.Column(
        db.Boolean, default=True
    )  # True for public, False for private
    image_url = db.Column(
        db.String(255)
    )  # You can use this field to store the URL of a court image
    number_of_courts = db.Column(
        db.Integer, default=1
    )  # You can set a default value here

    # Define a one-to-many relationship with HoursOfOperation
    hours_of_operation = db.relationship("HoursOfOperation", backref="court", lazy=True)

    def __init__(
        self,
        name=None,
        address=None,
        is_public=True,
        image_url=None,
        number_of_courts=1,
    ):
        self.name = name
        self.address = address
        self.is_public = is_public
        self.image_url = image_url
        self.number_of_courts = number_of_courts

    def __repr__(self):
        if self.name:
            return f"<Court {self.name}>"
        else:
            return f"{self.address}>"
