from flask import request
from flask_restful import Resource
from flask import jsonify
from database import db
from models.account import Account
from models.user import User

class AccountList(Resource):
    def get(self):
        try:
            accounts = Account.query.all()
            return jsonify({
                "status": "success",
                "data": [account.json() for account in accounts]
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

class AccountResource(Resource):
    def get(self, id):
        try:
            account = Account.query.get(id)
            if not account:
                return jsonify({"status": "error", "message": "Account not found"}), 404
            return jsonify({"status": "success", "data": account.json()})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

class AccountCreate(Resource):
    def post(self):
        data = request.get_json()  # Mengambil data JSON dari request body

        # Validasi input data
        if 'user_id' not in data or 'account_number' not in data or 'account_type' not in data:
            return {'message': 'Missing required fields'}, 400
        
        # Cek apakah user dengan user_id yang diberikan ada
        user = User.query.get(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404
        
        # Membuat objek Account baru
        new_account = Account(
            user_id=data['user_id'],
            account_number=data['account_number'],
            account_type=data['account_type'],
            balance=data.get('balance', 0.0)  # Menggunakan saldo default jika tidak ada
        )

        try:
            db.session.add(new_account)
            db.session.commit()
            return jsonify(new_account.json())
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

class AccountUpdate(Resource):
    def put(self, id):
        data = request.get_json()  # Mengambil data JSON dari request body

        if not data.get('account_number') or not data.get('account_type') or not data.get('balance'):
            return jsonify({"message": "Missing required fields"}), 400  # Return error jika ada yang kosong
        
        account = Account.query.get_or_404(id)  # Mengambil akun berdasarkan ID

        account.account_number = data['account_number']  # Memperbarui username
        account.account_type = data['account_type']  # Memperbarui email
        account.balance = data['balance']  # Memperbarui balance

       # Menyimpan perubahan ke database
        try:
            db.session.commit()  # Menyimpan perubahan
        except Exception as e:
            db.session.rollback()  # Jika terjadi kesalahan, rollback perubahan
            return jsonify({"message": str(e)}), 500  # Menampilkan error jika terjadi masalah saat menyimpan

        return jsonify(account.json())  # Mengembalikan data akun yang sudah diperbarui

class AccountDelete(Resource):
    def delete(self, id):
        account = Account.query.get_or_404(id)  # Mengambil akun berdasarkan ID
        db.session.delete(account)  # Menghapus akun dari database
        db.session.commit()  # Menyimpan perubahan ke database
        return {'message': 'Account deleted successfully'}, 200  # Menyatakan akun berhasil dihapus
