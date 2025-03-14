from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config
from database import db
from resources.user import UserRegister, UserMe, UserMeUpdate
from resources.account import AccountList, AccountResource, AccountCreate, AccountUpdate, AccountDelete
from resources.transaction import TransactionList, TransactionDetail, TransactionCreate 

app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi database
db.init_app(app)

api = Api(app)

# Tambahkan endpoint
api.add_resource(UserRegister, "/users")
api.add_resource(UserMe, '/users/<int:id>')
api.add_resource(UserMeUpdate, '/users/<int:id>')
api.add_resource(AccountList, '/accounts')  # GET /accounts
api.add_resource(AccountResource, '/accounts/<int:id>')  # GET /accounts/:id
api.add_resource(AccountCreate, '/accounts')  # POST /accounts
api.add_resource(AccountUpdate, '/accounts/<int:id>')  # PUT /accounts/:id
api.add_resource(AccountDelete, '/accounts/<int:id>')  # DELETE /accounts/:id
# Menambahkan route untuk Transaction Management
api.add_resource(TransactionList, '/transactions')
api.add_resource(TransactionDetail, '/transactions/<int:transaction_id>')
api.add_resource(TransactionCreate, '/transactions')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Membuat semua tabel dalam database jika belum ada
    app.run(debug=True)

