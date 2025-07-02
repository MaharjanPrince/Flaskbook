from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max= 50)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm = PasswordField('Confrim Password', validators=[
        DataRequired(), EqualTo('password', message="Passwords must match")
    ])
    Submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Log In')

    