from flask import (
    render_template, redirect, request, session, flash, url_for
)
from app import app, db
from models.games import Games
from models.users import Users


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


@app.route('/edit_game/<int:id>')
def edit(id):
    if 'logged_user' not in session or not session['logged_user']:
        flash('You must be logged to edit items')
        return redirect(url_for('login', next=url_for('edit', id=id)))

    game = Games.query.filter_by(id=id).first()

    return render_template('edit.html', title='Edit Game', game=game)


@app.route('/update', methods=['POST'])
def update():
    game = Games.query.filter_by(id=request.form['id']).first()
    game.name = request.form['name']
    game.category = request.form['category']
    game.console = request.form['console']

    db.session.add(game)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_user' not in session or not session['logged_user']:
        flash('You must be logged to edit items')
        return redirect(url_for('login'))

    game_name = Games.query.filter_by(id=id).first().name

    Games.query.filter_by(id=id).delete()
    db.session.commit()

    flash(f"The game {game_name.capitalize()} was deleted")

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
