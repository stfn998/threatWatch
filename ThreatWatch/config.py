import os

DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_SERVER = os.environ.get('DATABASE_SERVER')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
SECRET_KEY = os.environ.get('SECRET_KEY')

class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_NAME}'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
