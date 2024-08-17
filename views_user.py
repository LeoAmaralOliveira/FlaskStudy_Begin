from app import app
from flask import (
    render_template, redirect, request,
    session, flash, url_for
)
from models.users import Users
from helpers import UserForm
from flask_bcrypt import check_password_hash


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
