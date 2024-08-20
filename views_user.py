from app import app, db
from flask import (
    render_template, redirect, request,
    session, flash, url_for
)
from models.users import Users
from helpers import UserForm
from helpers import UserRegisterForm
from flask_bcrypt import check_password_hash, generate_password_hash


@app.route('/register')
def register():
    if 'logged_user' in session and session['logged_user']:
        flash(f"You're already logged on as {session['logged_user']}")
        return redirect(url_for('index'))
    form = UserRegisterForm()
    return render_template('register.html', form=form)


@app.route('/register_user', methods=['POST'])
def register_user():
    form = UserRegisterForm(request.form)

    if not form.validate_on_submit():
        flash('Passwords must match')
        return redirect(url_for('register'))

    name = form.name.data
    username = form.username.data
    pw = generate_password_hash(form.password.data)

    user = Users.query.filter_by(username=username).first()

    if user:
        flash("This user already exists!")
        return redirect(url_for('register'))

    new_user = Users(name=name, username=username, password=pw)
    db.session.add(new_user)
    db.session.commit()

    flash(f"{name} created successfully!")

    return redirect(url_for('login'))


@app.route('/login')
def login():
    if 'logged_user' in session and session['logged_user']:
        flash(f"You're already logged on as {session['logged_user']}")
        return redirect(url_for('index'))
    next = request.args.get('next')
    form = UserForm()
    return render_template('login.html', next=next, form=form)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    next = (
        request.form['next']
        if request.form['next'] != 'None'
        else url_for('index')
    )
    form = UserForm(request.form)

    username = form.username.data
    pw = form.password.data
    user = Users.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, pw):
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
    if 'logged_user' not in session or not session['logged_user']:
        flash("You're not connected to an account")
        return redirect(url_for('index'))
    session['logged_user'] = None
    flash('Logout successful')

    return redirect(url_for('index'))
