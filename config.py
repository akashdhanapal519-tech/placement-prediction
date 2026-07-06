import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'placement_secret_key_2025_xk9!')
    DATABASE = os.path.join(os.path.dirname(__file__), 'placement.db')
    DEBUG = True
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'
