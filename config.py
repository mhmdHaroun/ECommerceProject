import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///ecommerce.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'mosalehsecretKey'     #i used short admin token just to make testing simple but provided tokenes are much much longer  
    JWT_SECRET_KEY = 'mosalehsecretKey'