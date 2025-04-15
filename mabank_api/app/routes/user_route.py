# app/routes/user_route.py

from flask import Blueprint, request
from flask_restful import Api, Resource
from app.services.user_service import UserService
from app.decorators.token_required import token_required

# Inisialisasi Blueprint dan API
user_bp = Blueprint('user', __name__)
api = Api(user_bp)

class UserRegister(Resource):
    def post(self):
        user_service = UserService()
        data = request.get_json()
        return user_service.create_user(data)

class UserLogin(Resource):
    def post(self):
        user_service = UserService()
        data = request.get_json()
        return user_service.login_user(data)
    
class UserList(Resource):
    def get(self):
        user_service = UserService()
        return user_service.get_all_users()

class UserMe(Resource):
    def get(self, user_id):
        user_service = UserService()
        return user_service.get_user_profile(user_id)

class UserMeUpdate(Resource):
    def put(self, user_id):
        data = request.get_json()
        user_service = UserService()
        return user_service.update_user_profile(user_id, data)
    
class DeleteUser(Resource):
    def delete(self, user_id):
        user_service = UserService()
        return user_service.delete_user(user_id)

# Menambahkan Resource ke API
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserList, '/users')
api.add_resource(UserMe, '/users/<int:user_id>')
api.add_resource(UserMeUpdate, '/users/<int:user_id>')
api.add_resource(DeleteUser, '/users/<int:user_id>')
