from flask import request, jsonify
from flask_restful import Resource
from database import db
from models.transaction import Transaction
from models.account import Account
from datetime import datetime

# GET /transactions: Retrieve a list of all transactions
class TransactionList(Resource):
    def get(self):
        try:
            account_id = request.args.get('account_id', type=int)
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            query = Transaction.query

            if account_id:
                query = query.filter_by(account_id=account_id)

            if start_date:
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    query = query.filter(Transaction.date >= start_date)
                except ValueError:
                    return {"message": "Invalid start_date format. Use YYYY-MM-DD."}, 400

            if end_date:
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    query = query.filter(Transaction.date <= end_date)
                except ValueError:
                    return {"message": "Invalid end_date format. Use YYYY-MM-DD."}, 400

            transactions = query.all()
            return jsonify({"status": "success", "data": [transaction.json() for transaction in transactions]})
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500

# GET /transactions/:id: Retrieve details of a specific transaction by its ID
class TransactionDetail(Resource):
    def get(self, transaction_id):
        try:
            transaction = Transaction.query.get(transaction_id)
            if not transaction:
                return {"message": "Transaction not found"}, 404

            return jsonify({
                "id": transaction.id,
                "account": {
                    'id': transaction.account.id,
                    'user': {
                        'id': transaction.account.user.id,
                        'username': transaction.account.user.username,
                        'email': transaction.account.user.email
                    },
                    'account_number': transaction.account.account_number,
                    'account_type': transaction.account.account_type,
                    'balance': transaction.account.balance
                },
                "amount": transaction.amount,
                "type": transaction.type,
                "date": transaction.date.isoformat()
            })
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500
        
# POST /transactions: Initiate a new transaction (deposit, withdrawal, or transfer)
class TransactionCreate(Resource):
    def post(self):
        try:
            data = request.get_json()

            required_fields = ['account_id', 'type', 'amount']
            for field in required_fields:
                if field not in data:
                    return {"message": f"Missing required field: {field}"}, 400

            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return {"message": "Amount must be greater than zero"}, 400
            except ValueError:
                return {"message": "Invalid amount format"}, 400

            account = Account.query.get(data['account_id'])
            if not account:
                return {"message": "Account not found"}, 404

            transaction_type = data['type'].lower()
            if transaction_type not in ['deposit', 'withdrawal', 'transfer']:
                return {"message": "Invalid transaction type"}, 400

            # Handling different transaction types
            if transaction_type == 'deposit':
                account.balance += amount

            elif transaction_type == 'withdrawal':
                if account.balance < amount:
                    return {"message": "Insufficient funds"}, 400
                account.balance -= amount

            elif transaction_type == 'transfer':
                if 'destination_account_id' not in data:
                    return {"message": "Missing destination_account_id for transfer"}, 400

                destination_account = Account.query.get(data['destination_account_id'])
                if not destination_account:
                    return {"message": "Destination account not found"}, 404

                if destination_account.id == account.id:
                    return {"message": "Cannot transfer to the same account"}, 400

                if account.balance < amount:
                    return {"message": "Insufficient funds for transfer"}, 400

                account.balance -= amount
                destination_account.balance += amount

            # Create transaction record
            new_transaction = Transaction(
                account_id=account.id,
                type=transaction_type,
                amount=amount,
                date=datetime.utcnow()
            )

            db.session.add(new_transaction)
            db.session.commit()

            return jsonify({
                "message": "Transaction created successfully",
                "transaction": {
                    "id": new_transaction.id,
                    "account_id": new_transaction.account_id,
                    "type": new_transaction.type,
                    "amount": new_transaction.amount,
                    "date": new_transaction.date.isoformat()
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Server error: {str(e)}"}, 500
