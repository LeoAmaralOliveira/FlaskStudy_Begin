from pathlib import os
from dotenv import load_dotenv
from flask import (
    Flask, render_template, redirect, request, session, flash, url_for
)
from flask_sqlalchemy import SQLAlchemy


load_dotenv()
app = Flask(__name__)
app.secret_key = str(os.getenv("FLASK_SECRET_KEY"))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://'
    f'{str(os.getenv("MYSQL_USERNAME"))}:'
    f'{str(os.getenv("MYSQL_PW"))}@'
    f'{str(os.getenv("MYSQL_HOST"))}/gameteca'
)
db = SQLAlchemy(app)


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Name {self.name}>'


class Users(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Name {self.name}>'


@app.route('/')
def index():
    game_list = Games.query.order_by(Games.id)
    return render_template('list.html', title='Games', games=game_list)


@app.route('/new_game')
def new():
    if 'logged_user' not in session or not session['logged_user']:
        flash('You must be logged to add new items')
        return redirect(url_for('login', next=url_for('new')))

    return render_template('new.html', title='New Game')


@app.route('/create_game', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    game = Games.query.filter_by(name=name).first()
    if game:
        flash('The game already exists')
        return redirect(url_for('new'))

    new_game = Games(name=name, category=category, console=console)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    next = (
        request.form['next']
        if request.form['next'] != 'None'
        else url_for('index')
    )
    username = request.form['username']
    pw = request.form['password']
    user = Users.query.filter_by(username=username).first()
    if user:
        if pw == user.password:
            session['logged_user'] = user.name
            flash(f"{session['logged_user']} successfully logged in")
            return redirect(next)

    flash("Log In Failed! Try Again")
    if not next:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login', next=next))


@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('Logout successful')

    return redirect(url_for('index'))


app.run(host='0.0.0.0', port=8000, debug=True)
