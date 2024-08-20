from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from prepare_db import init_db


init_db()


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


from views_game import * # NoQA
from views_user import * # NoQA


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
