import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///revo_bank.db'  # Ganti dengan PostgreSQL jika perlu
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"  # Untuk JWT Authentication
