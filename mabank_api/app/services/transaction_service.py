from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from database import db
from app.models.account_model import Account
from app.models.transaction_model import Transaction
from decimal import Decimal
from app.decorators.token_required import token_required

class TransactionService:

    @staticmethod
    @token_required
    def create_transaction(data) :
        try:
             # Validasi jika akun pengirim dan penerima ada
            from_account = Account.query.get(data["from_account_id"])
            to_account = Account.query.get(data["to_account_id"])


            if not from_account or not to_account:
                raise ValueError("Akun pengirim atau penerima tidak ditemukan.")

            # Validasi saldo cukup
            if from_account.balance < data["amount"]:
                raise ValueError("Saldo tidak cukup untuk transaksi ini.")
            
            # Membuat transaksi baru
            new_transaction = Transaction(
                from_account_id=data["from_account_id"],
                to_account_id=data["to_account_id"],
                amount = data["amount"],
                type=data["type"],
                description=data["description"],
                created_at=datetime.utcnow()
            )
            amount = Decimal(str(data["amount"]))  # konversi dengan aman

             # Perbarui saldo akun pengirim dan penerima
            from_account.balance -= amount
            to_account.balance += amount

             # Simpan transaksi dan pembaruan saldo ke dalam database
            db.session.add(new_transaction)
            db.session.commit()

            return {"status":"success","message": "Transaction created", "data": new_transaction.json()}, 201
        except ValueError as ve:
            db.session.rollback()
            raise ve
        except SQLAlchemyError as e:
            db.session.rollback()   
            raise Exception(f"Terjadi kesalahan saat memproses transaksi: {str(e)}")
    
    @staticmethod
    @token_required
    def get_transactions_by_account(account_id):
        try:
            # Mendapatkan semua transaksi yang melibatkan akun tertentu
            transactions = Transaction.query.filter(
                (Transaction.from_account_id == account_id) | 
                (Transaction.to_account_id == account_id)
            ).all()
            return transactions
        except SQLAlchemyError as e:
            raise Exception("Terjadi kesalahan saat mengambil transaksi.")
    
    @staticmethod
    @token_required
    def get_transaction_by_id(transaction_id):
        try:
            # Mendapatkan transaksi berdasarkan ID
            transaction = Transaction.query.get(transaction_id)
            if not transaction:
                return {"message": "Transaksi tidak ditemukan."}, 404
            
            return {"status": "success", "data": transaction.json()}, 200
        
        except ValueError as ve:
            raise ve
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
    
    @staticmethod
    @token_required
    def get_all_transaction():
        try:
            transactions = Transaction.query.all()

            if not transactions:
                return{"message": "No Transactions found"}, 404
            
            return {"status": "success", "message": "All Transactions", "data" : [transaction.json() for transaction in transactions]}, 200
        
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
        
    @staticmethod
    @token_required
    def delete_transaction(transaction_id):
        try:
            transaction = Account.query.get(transaction_id)

            if not transaction:
                return {"message": "Account not found"}, 404

            db.session.delete(transaction)
            db.session.commit()

            return {"status": "success", "message": "Transaction deleted successfully"}, 200

        except Exception as e:
            return {"status": "error", "message": "Failed to delete transaction", "error": str(e)}, 500
