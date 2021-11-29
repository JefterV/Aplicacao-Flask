from flask import Flask
from flask_mysqldb import MySQL


# INIT CODE
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = MySQL(app)

from views import *

# EXECUTANDO SERVIÇO
if __name__ == '__main__': 
    app.run(debug=True)