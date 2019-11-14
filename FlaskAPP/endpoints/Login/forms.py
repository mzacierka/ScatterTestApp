from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Must be a valid email with containing @ and .'), Email()])
    password = PasswordField('Password', validators=[DataRequired('Fill this out')])

    submit = SubmitField('Log in')


class ForgotEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('enter a valid email address'), Email()])

    submit = SubmitField('Reset Password')


class ResetEmailForm(FlaskForm):
    password_first = PasswordField('Enter Password', validators=[DataRequired('Fill this out')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired('Fill this out')])

    submit = SubmitField('Reset Password')
