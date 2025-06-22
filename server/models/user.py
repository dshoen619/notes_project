from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    
    # JWT token fields
    token = db.Column(db.String(500), nullable=True)
    token_expires_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'
    
    def generate_token(self, secret_key=None):
        """Generate a JWT token for the user"""
        if not secret_key:
            secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
        
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        
        # Store token in database
        self.token = token
        self.token_expires_at = payload['exp']
        db.session.commit()
        
        return token
    
    def validate_token(self, token, secret_key=None):
        """Validate if the provided token is valid for this user"""
        if not secret_key:
            secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
        
        try:
            # Decode the token
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            # Check if token belongs to this user
            if payload['user_id'] != self.id:
                return False
            
            # Check if token is expired
            if datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(payload['exp']):
                return False
            
            return True
            
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
    
    def revoke_token(self):
        """Revoke the current token for the user"""
        self.token = None
        self.token_expires_at = None
        db.session.commit()
    
    def is_token_valid(self):
        """Check if the stored token is still valid"""
        if not self.token or not self.token_expires_at:
            return False
        
        return datetime.datetime.utcnow() < self.token_expires_at 