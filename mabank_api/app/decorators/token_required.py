from functools import wraps
from flask import request, jsonify
import jwt
from app import Config
from app.models.user_model import User

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')  # Mengambil token dari header

        if not token:
            return {"message": "Token is missing!"}, 403

        try:
            # Menghapus 'Bearer ' jika ada
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token['user_id']

            # Menyimpan user_id dalam request untuk digunakan di endpoint
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found!"}, 404

            request.user = user  # Menyimpan user di request
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired!"}, 403
        except jwt.InvalidTokenError:
            return {"message": "Invalid token!"}, 403
        except Exception as e:
            # Menangani exception lain yang mungkin terjadi
            return {"message": "Internal server error", "error": str(e)}, 500
        return f(*args, **kwargs)

    return decorated_function
