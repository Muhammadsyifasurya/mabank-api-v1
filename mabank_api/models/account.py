from database import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    account_type = db.Column(db.String(50), nullable=False)  # Menambahkan kolom balance

    user = db.relationship('User', backref=db.backref('accounts', lazy=True))


    def json(self):
        return {
            'id': self.id,
            'user': {
                'id':self.user.id,
                'username': self.user.username,
                'email' : self.user.email
            },
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance
        }
    
    def __repr__(self):
        return f'<Account {self.account_number}>'

    
