from database import db
from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(DATETIME, default=datetime.utcnow, nullable=False)  # timestamp saat pembuatan
    updated_at = db.Column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # timestamp untuk pembaruan

    def json(self):
        return {
            "user_id": self.user_id, 
            "username": self.username, 
            "email": self.email, 
            "created_at": self.created_at.isoformat() if self.created_at else None,  # Mengonversi datetime ke string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # Mengonversi datetime ke string
            }
    
    def __repr__(self):
        return f'<User {self.username}>'
