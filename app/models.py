from .database import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Apartment(db.Model):
    apt_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    rent = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    utilities = db.Column(db.String(500))
    university_name = db.Column(db.String(200), nullable=False)
    photos = db.Column(db.String(500))  # Store photo URLs or paths
    contact = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    user = db.relationship('User', back_populates='apartments')

User.apartments = db.relationship('Apartment', back_populates='user', cascade="all, delete-orphan")
