import os
import psycopg2


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('USER_NAME')
    MAIL_PASSWORD = os.environ.get('USER_PASSWORD')
    MAIL_DEFAULT_SENDER = 'noreply@gmail.com'
    SECURITY_EMAIL_SENDER = 'noreply@gmail.com'
    DEBUG = True

class S3Config:
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = f'https://{S3_BUCKET}.s3.amazonaws.com/'
