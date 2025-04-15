# app/services/user_service.py
from flask import current_app
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import User
from datetime import datetime, timedelta
from database import db
from app.decorators.token_required import token_required

class UserService:
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(hours=2)
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            return token
        except Exception as e:
            return None

    @staticmethod
    def login_user(data):
        try:
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {"message": "Email and password are required"}, 400

            user = User.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password_hash, password):
                return {"message": "Invalid email or password"}, 401

            token = UserService.generate_token(user.user_id)

            if not token:
                return {"message": "Token generation failed"}, 500

            return {
                "status": "success",
                "message": "Login successful",
                "token": token,
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email
                }
            }, 200

        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500

    @staticmethod
    def create_user(data):
        """Membuat pengguna baru dan menyimpannya ke database"""
        try:
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Validasi input data
            if not username or not email or not password:
                return {"message": "Username, email, and password are required"}, 400

            # Cek apakah email sudah terdaftar
            if User.query.filter_by(email=email).first():
                return {"message": "Email already registered"}, 400
            
            password_hash = generate_password_hash(password)  # Meng-hash password
            
            # Membuat pengguna baru dan menyimpannya
            user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()

            return {"status": "success", "message": "User created successfully", "data": {"username": user.username, "email": user.email}}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": "Internal server error", "error": str(e)}, 500

    @staticmethod
    @token_required
    def get_all_users():
        try:
            users = User.query.all()

            if not users:
                return{"message": "No Users found"}, 404
            
            users_list = [{"user_id": user.user_id, "username": user.username, "email": user.email} for user in users]
            
            return {"status": "success", "message": "All Users list", "data" : users_list}, 200
        
        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
        
    @staticmethod
    @token_required
    def get_user_profile(user_id):
        """Mengambil profil pengguna berdasarkan ID pengguna"""
        try:
            # Mengambil informasi pengguna berdasarkan ID
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            return {"status": "success", "data": user.json()}, 200

        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500
            
    @staticmethod
    @token_required
    def update_user_profile(user_id, data):
        """Memperbarui profil pengguna"""
        try:
            # Mengambil pengguna berdasarkan ID
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            
            # Memperbarui data pengguna
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)

            # Memperbarui password jika disertakan
            if data.get('password'):
                user.password_hash = generate_password_hash(data['password'])
            user.updated_at = datetime.utcnow()

            db.session.commit()
            return {"status": "success", "message": "User profile updated successfully", "data": user.json()}, 200
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Internal server error", "error": str(e)}, 500

    @staticmethod
    @token_required
    def delete_user(user_id):
        try:
            # Mengambil pengguna berdasarkan ID
            user = User.query.get(user_id)

            if not user:
                return {"message": "User not found"}, 404
            
            db.session.delete(user)
            db.session.commit()
            return {"status": "success", "message": "User deleted successfully"}, 200

        except Exception as e:
            return {"status": "error", "message": "Failed to delete user", "error": str(e)}, 500

            
        