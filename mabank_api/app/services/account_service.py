from app.models.user_model import User, db
from app.models.account_model import Account
from datetime import datetime
from database import db
from app.decorators.token_required import token_required

class AccountService:

    @staticmethod
    @token_required
    def create_account(data):
        try:
            user_id = data.get('user_id')
            if not user_id :
                return {"message": "User not found"}, 404
            
             # Pastikan account_number unik
            existing_account = Account.query.filter_by(account_number=data.get('account_number')).first()
            if existing_account:
                return {"message": "Account number already exists"}, 400
        
            new_account = Account(
                user_id = user_id,
                account_type=data.get('account_type'),
                account_number=data.get('account_number'),
                balance=data.get('balance'),
            )

            db.session.add(new_account)
            db.session.commit()

            return {"status":"success","message": "Account created", "data": new_account.json()}, 201
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500

    @staticmethod
    @token_required
    def get_all_account():
        try:
            accounts = Account.query.all()

            if not accounts:
                return{"message": "No Accounts found"}, 404
            
            return {"status": "success", "message": "All Accounts list", "data" : [account.json() for account in accounts]}, 200
        
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500

    @staticmethod
    @token_required
    def get_account(account_id):
        try:
            # Mengambil akun berdasarkan ID
            account = Account.query.get(account_id)
            if not account:
                return {"message": "Account not found"}, 404

            return {"status": "success", "data": account.json()}, 200
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
        
    @staticmethod
    @token_required
    def get_accounts_by_user(user_id):
        try:
            # Mengambil akun berdasarkan ID
            accounts = Account.query.filter_by(user_id=user_id).all()
            if not accounts:
                return {"message": "Account not found"}, 404
            
            user_data = accounts[0].user.json() 

            account_list = [
                {
                    "id": account.id,
                    "account_type": account.account_type,
                    "account_number": account.account_number,
                    "balance": float(account.balance),
                    "created_at": account.created_at.isoformat(),
                    "updated_at": account.updated_at.isoformat()
                }
                for account in accounts
            ]
            
            return {
                "status": "success", 
                "data": {
                    "user": user_data,
                    "accounts": account_list
                }
            }, 200
        
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
        
    @staticmethod
    @token_required
    def delete_account(account_id):
        try:
            account = Account.query.get(account_id)

            if not account:
                return {"message": "Account not found"}, 404

            db.session.delete(account)
            db.session.commit()

            return {"status": "success", "message": "Account deleted successfully"}, 200

        except Exception as e:
            return {"status": "error", "message": "Failed to delete account", "error": str(e)}, 500

    @staticmethod
    @token_required
    def update_account(account_id, data):
        try:
            account = Account.query.get(account_id)
            
            if not account:
                return {"message": "Account not found"}, 404

            # Update field jika ada di data
            if "account_type" in data:
                account.account_type = data["account_type"]
            if "account_number" in data:
                existing = Account.query.filter_by(account_number=data["account_number"]).first()
                if existing and existing.id != account.id:
                    return {"message": "Account number already exists"}, 400
            account.account_number = data["account_number"]

            if "balance" in data:
                account.balance = data["balance"]

            db.session.commit()

            return {
                "status": "success",
                "message": "Account updated successfully",
                "data": account.json()
            }, 200

        except Exception as e:
            return {"status": "error", "message": "Failed to update account", "error": str(e)}, 500
