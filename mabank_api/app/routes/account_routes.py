from flask import Blueprint, request
from flask_restful import Api, Resource
from app.services.account_service import AccountService

# Inisialisasi Blueprint dan API
account_bp = Blueprint('account', __name__)
api = Api(account_bp)

class CreateAccount(Resource):
    def post(self):
        account_service = AccountService()
        data = request.get_json()
        return account_service.create_account(data)

class AccountList(Resource):
    def get(self):
        account_service = AccountService()
        return account_service.get_all_account()
    
class Account(Resource):
    def get(self, id):
        account_service = AccountService()
        return account_service.get_account(id)
    
class AccountUser(Resource):
    def get(self, user_id):
        account_service = AccountService()
        return account_service.get_accounts_by_user(user_id)

class DeleteAccount(Resource):
    def delete(self, account_id):
        account_service = AccountService()
        return account_service.delete_account(account_id)
    
class UpdateAccount(Resource):
    def put(self, account_id):
        account_service = AccountService()
        data = request.get_json()
        return account_service.update_account(account_id, data)
    
api.add_resource(AccountUser, '/users/<string:user_id>/accounts')
api.add_resource(AccountList, '/accounts')
api.add_resource(CreateAccount, '/accounts')
api.add_resource(Account, '/accounts/<string:id>')
api.add_resource(DeleteAccount, "/accounts/<int:account_id>")
api.add_resource(UpdateAccount, "/accounts/<int:account_id>")
