from flask import (
    render_template, redirect, request,
    session, flash, url_for,
    send_from_directory
)
from app import app, db
from models.games import Games
from helpers import recover_image, delete_image, GameForm
import time


@app.route('/')
def index():
    game_list = Games.query.order_by(Games.id)
    logged_msg = None
    if 'logged_user' in session and session['logged_user']:
        logged_msg = f"Welcome, {session['logged_user']}"

    return render_template(
        'list.html', title='Games', logged_msg=logged_msg, games=game_list
    )


@app.route('/new_game')
def new():
    if 'logged_user' not in session or not session['logged_user']:
        flash('You must be logged to add new items')
        return redirect(url_for('login', next=url_for('new')))

    form = GameForm()

    return render_template('new.html', title='New Game', form=form)


@app.route('/create_game', methods=['POST'])
def create():
    form = GameForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('new'))

    name = form.name.data
    category = form.category.data
    console = form.console.data

    game = Games.query.filter_by(name=name).first()
    if game:
        flash('The game already exists')
        return redirect(url_for('new'))

    new_game = Games(name=name, category=category, console=console)
    db.session.add(new_game)
    db.session.commit()

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    if file:
        file.save(f'{upload_path}/game_{new_game.id}_{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/edit_game/<int:id>')
def edit(id):
    if 'logged_user' not in session or not session['logged_user']:
        flash('You must be logged to edit items')
        return redirect(url_for('login', next=url_for('edit', id=id)))

    game = Games.query.filter_by(id=id).first()
    form = GameForm()
    form.name.data = game.name
    form.category.data = game.category
    form.console.data = game.console
    game_image = recover_image(id)

    return render_template(
        'edit.html',
        title='Edit Game',
        id=id,
        game_image=game_image,
        form=form
    )


@app.route('/update', methods=['POST'])
def update():
    form = GameForm(request.form)

    if form.validate_on_submit():
        game = Games.query.filter_by(id=request.form['id']).first()
        game.name = form.name.data
        game.category = form.category.data
        game.console = form.console.data

        db.session.add(game)
        db.session.commit()

        file = request.files['file']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        delete_image(game.id)
        file.save(f'{upload_path}/game_{game.id}_{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_user' not in session or not session['logged_user']:
        flash('You must be logged to edit items')
        return redirect(url_for('login'))

    game_name = Games.query.filter_by(id=id).first().name

    Games.query.filter_by(id=id).delete()
    db.session.commit()
    delete_image(id)

    flash(f"The game {game_name.capitalize()} was deleted")

    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)
