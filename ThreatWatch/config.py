import os

DATABASE_SERVER = '(localdb)\\MSSQLLocalDB'
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_DRIVER = os.environ.get('DATABASE_DRIVER')

class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = f'mssql://@{DATABASE_SERVER}/{DATABASE_NAME}?driver={DATABASE_DRIVER}'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
