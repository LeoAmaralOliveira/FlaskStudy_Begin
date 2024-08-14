from pathlib import os
from dotenv import load_dotenv
from flask import (
    Flask, render_template, redirect, request, session, flash, url_for
)
from models.game import Game
from models.user import User


load_dotenv()
game_list = []
users = {}
app = Flask(__name__)
app.secret_key = str(os.getenv('FLASK_SECRET_KEY'))


@app.route('/')
def index():
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

    game_list.append(Game(name, category, console))

    return redirect(url_for('index'))


@app.route('/register')
def register():
    if 'logged_user' not in session or not session['logged_user']:
        return render_template('register.html', title='Register User')

    flash("You're already logged in")
    return redirect(url_for('index'))


@app.route('/save_user', methods=['POST'])
def save_user():
    username = request.form['username']
    nickname = request.form['nickname']
    password = request.form['password']
    password2 = request.form['password2']

    if password != password2:
        flash('Passwords do not match! Try again')
        return redirect(url_for('register'))
    if username in users:
        flash('This user already exists!')
        return redirect(url_for('register'))

    user = User(username, nickname, password)
    users[user.username] = user

    return redirect(url_for('login', next=url_for('index')))


@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    pw = request.form['password']
    if username in users:
        if pw == users[username].password:
            session['logged_user'] = users[username].nickname
            flash(f"{session['logged_user']} successfully logged in")
            next = request.form['next']
            return redirect(next)

    flash("Log In Failed! Try Again")
    next = request.form['next']
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
