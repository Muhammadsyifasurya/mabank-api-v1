from flask import request, jsonify
from flask_restful import Resource
from database import db
from models.user import User

class UserRegister(Resource):
    def post(self):
        try:
            data = request.get_json()

            # Validasi input data
            if not data:
                return {"message": "Request body is missing"}, 400

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return {"message": "Username, email, and password are required"}, 400

            # Cek apakah email sudah digunakan
            if User.query.filter_by(email=email).first():
                return {"message": "Email already registered"}, 400

            # Simpan pengguna baru
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully"}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": "Internal server error", "error": str(e)}, 500
    
    def get(self):
        try:
            users = User.query.all()

            if not users:
                return {"message": "No users found"}, 404

            user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]

            return {"status": "success", "users": user_list}, 200

        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
    
    
class UserMe(Resource):    
    def get(self, id):
        try:
            user = User.query.get(id)
            if not user:
                return {"message": "User not found"}, 404

            return jsonify({"status": "success","data": user.json()})

        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
    
class UserMeUpdate(Resource):
    def put(self, id):
        try:
            data = request.get_json()

            if not data or 'id' in data:
                return {"message": "User ID is not required"}, 400

            user = User.query.get(id)

            if not user:
                return {"message": "User not found"}, 404

            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)

            db.session.commit()
            return {"message": "User updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "Internal server error", "error": str(e)}, 500
