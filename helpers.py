import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class GameForm(FlaskForm):
    name = StringField(
        'Name',
        [validators.DataRequired(), validators.Length(min=1, max=50)]
    )
    category = StringField(
        'Category',
        [validators.DataRequired(), validators.Length(min=1, max=40)]
    )
    console = StringField(
        'Console',
        [validators.DataRequired(), validators.Length(min=1, max=20)]
    )
    save = SubmitField('Save')


class UserForm(FlaskForm):
    username = StringField(
        'Username',
        [validators.DataRequired(), validators.Length(min=1, max=20)]
    )
    password = PasswordField(
        'Password',
        [validators.DataRequired(), validators.Length(min=1, max=100)]
    )
    login = SubmitField('Login')


class UserRegisterForm(FlaskForm):
    name = StringField(
        'Name',
        [validators.DataRequired(), validators.Length(min=1, max=20)]
    )
    username = StringField(
        'Username',
        [validators.DataRequired(), validators.Length(min=1, max=20)]
    )
    password = PasswordField(
        'Password',
        [
            validators.DataRequired(),
            validators.Length(min=1, max=100),
            validators.EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField('Repeat Password')
    register = SubmitField('Register')


def recover_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'game_{id}' in filename:
            return filename

    return 'capa_padrao.jpg'


def delete_image(id):
    filename = recover_image(id)
    if filename != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
