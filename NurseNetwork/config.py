#!/usr/bin/python3

import os


MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PWD = os.getenv('MYSQL_PWD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'\
    .format(MYSQL_USER,MYSQL_PWD,MYSQL_HOST,MYSQL_DB)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
