from flask import Blueprint, request
from flask_restful import Api, Resource
from app.services.transaction_service import TransactionService

# Inisialisasi Blueprint dan API
transaction_bp = Blueprint('transaction', __name__)
api = Api(transaction_bp)

class CreateTransaction(Resource):
    def post(self):
        transaction_service = TransactionService()
        data = request.get_json()
        return transaction_service.create_transaction(data)

class TransactionList(Resource):
    def get(self):
        transaction_service = TransactionService()
        return transaction_service.get_all_transaction()

class TransactionDetail(Resource):
    def get(self, transaction_id):
        transaction_service = TransactionService()
        return transaction_service.get_transaction_by_id(transaction_id)

class DeleteTransaction(Resource):
    def delete(self, transaction_id):
        transaction_service = TransactionService()
        return transaction_service.delete_transaction(transaction_id)

api.add_resource(CreateTransaction, '/transaction')
api.add_resource(TransactionList, '/transactions')
api.add_resource(TransactionDetail, '/transactions/<int:transaction_id>')
api.add_resource(DeleteTransaction, '/transactions/<int:transaction_id>')
