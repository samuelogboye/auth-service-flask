'''Database Model structured'''
from werkzeug.security import generate_password_hash, check_password_hash
from auth import db
from .base import BaseModel

class User(BaseModel):
    '''User Table'''
    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

    def set_password(self, password):
        '''Set password for the user'''
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        '''Check if the provided password matches the stored password'''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        '''Return a string representation of the user object'''
        return f"User('{self.username}', '{self.email}', '{self.created_at}')"

    def format(self):
        '''Return a dictionary representation of the user object'''
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }
