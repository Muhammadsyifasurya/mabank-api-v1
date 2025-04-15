from database import db
from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime
from sqlalchemy.orm import relationship

from app.models.transaction_model import Transaction

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)  # Menambahkan kolom balance
    account_number = db.Column(db.String(255), unique=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.0)
    created_at = db.Column(DATETIME, default=datetime.utcnow, nullable=False)  # timestamp saat pembuatan
    updated_at = db.Column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # timestamp untuk pembaruan

    # Relationship ke User
    user = db.relationship('User', backref=db.backref('accounts', lazy=True))
    
        # Relationship ke Transactions (pengirim dan penerima)
    from_transactions = relationship('Transaction', foreign_keys=[Transaction.from_account_id])
    to_transactions = relationship('Transaction', foreign_keys=[Transaction.to_account_id])
    
    def json(self):
        return {
            'id': self.id,
            'user': {
                'user_id':self.user.user_id,
                'username': self.user.username,
                'email' : self.user.email
            },
            'account_type': self.account_type,
            'account_number': self.account_number,
            'balance': float(self.balance),
            "created_at": self.created_at.isoformat() if self.created_at else None,  # Mengonversi datetime ke string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # Mengonversi datetime ke string
        }
    
    def __repr__(self):
        return f'<Account {self.account_number} - {self.account_type}>' 
