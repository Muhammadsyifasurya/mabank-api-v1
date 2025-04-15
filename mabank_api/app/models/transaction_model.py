from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from database import db  # Ganti dengan nama yang sesuai pada project kamu

class Transaction(db.Model):    
    transaction_id = db.Column(Integer, primary_key=True)
    from_account_id = db.Column(Integer, ForeignKey('account.id'), nullable=True)  # Account yang mengirim
    to_account_id = db.Column(Integer, ForeignKey('account.id'), nullable=True)  # Account yang menerima
    amount = db.Column(DECIMAL(10, 2), nullable=False)
    type = db.Column(String(255), nullable=False)  # e.g., "deposit", "withdrawal", "transfer"
    description = db.Column(String(255), nullable=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationship ke Account (One-to-Many)
    from_account = db.relationship('Account', foreign_keys=[from_account_id], back_populates='from_transactions')
    to_account = db.relationship('Account', foreign_keys=[to_account_id], back_populates='to_transactions')

    def json(self):
        return {
            'transaction_id': self.transaction_id,
            'from_account_id': self.from_account_id,
            'to_account_id': self.to_account_id,
            'amount': float(self.amount),
            'type': self.type,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Transaction({self.transaction_id}, {self.from_account_id}, {self.to_account_id}>'