# import os
# import tempfile
#
# db_fd, db_path = tempfile.mkstemp()
# path = os.path.join(os.environ["HOMEPATH"], 'desktop','site.db')
#
# class Config_test:
#     SECRET_KEY = "BAD_SECRET_KEY"
#     SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_URL")
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('USER_NAME')
#     MAIL_PASSWORD = os.environ.get('USER_PASSWORD')
#     MAIL_DEFAULT_SENDER = 'noreply@gmail.com'
#     SECURITY_EMAIL_SENDER = 'noreply@gmail.com'
#     Testing = True
#     WTF_CSRF_ENABLED = False
#
