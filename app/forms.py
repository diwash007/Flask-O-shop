from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired(), Length(max=50)])
	phone = StringField("Phone No:", validators=[DataRequired(), Length(max=30)])
	email = StringField("Email:", validators=[DataRequired(), Email()])
	password = PasswordField("Password:", validators=[DataRequired(), Regexp("^[a-zA-Z0-9_\-&$@#!%^*+.]{8,30}$", message='Password must be 8 characters long and should contain letters, numbers and symbols.')])
	confirm = PasswordField("Confirm Password:",validators=[EqualTo('password', message='Passwords must match')])
	submit = SubmitField("Register")