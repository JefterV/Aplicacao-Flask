import os
from datetime import timedelta

SECRET_KEY = 'XYZ'

MYSQL_HOST     = '127.0.0.1'
MYSQL_USER     = 'root2'
MYSQL_PASSWORD = 'root2'
MYSQL_DB = 'JOGOTECA'
MYSQL_PORT     = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
