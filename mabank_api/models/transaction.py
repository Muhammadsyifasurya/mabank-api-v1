from datetime import datetime
from database import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False) 
    
    # Relasi dengan Account (asumsi sudah ada model Account)
    account = db.relationship('Account', backref=db.backref('transactions', lazy=True))

    def json(self):
        return {
            'id': self.id,
            'account': {
                'id':self.account.id,
                'user': {
                    'id':self.account.user.id,
                    'username': self.account.user.username,
                    'email' : self.account.user.email
                },
                'account_number': self.account.account_number,
                'account_type': self.account.account_type,
                'balance': self.account.balance
            },
            'amount': self.amount,
            'date': self.date.isoformat(),  # Mengonversi datetime menjadi string yang sesuai format ISO
            'type': self.type  # Menambahkan jenis transaksi
        }
    
    def __repr__(self):
        return f"<Transaction {self.id} - {self.type} - {self.amount}>"
