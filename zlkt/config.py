import os

DEBUG = True
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/mark'
SQLALCHEMY_TRACK_MODIFICATIONS = False
