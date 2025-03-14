from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def json(self):
        return {"id": self.id, "username": self.username, "email": self.email}
    
    def __repr__(self):
        return f'<User {self.username}>'
    