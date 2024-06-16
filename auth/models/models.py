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
    refresh_tokens = db.relationship('RefreshToken', backref='user', lazy=True)

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

class RefreshToken(BaseModel):
    '''Refresh Token Table'''
    __tablename__ = 'refreshtokens'

    token = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        '''Return a string representation of the refresh token object'''
        return f"RefreshToken('{self.token}', '{self.user_id}', '{self.expires_at}')"

    def format(self):
        '''Return a dictionary representation of the refresh token object'''
        return {
            'token': self.token,
            'user_id': self.user_id,
            'used': self.used,
            'expires_at': self.expires_at
        }
