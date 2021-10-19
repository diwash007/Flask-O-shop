from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")

class RegisterForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired(), Length(max=50)])
	phone = StringField("Phone No:", validators=[DataRequired(), Length(max=30)])
	email = StringField("Email:", validators=[DataRequired(), Email(), Length(max=50)])
	password = PasswordField("Password:", validators=[DataRequired(), Length(max=50)])
	confirm = PasswordField("Confirm Password:",validators=[EqualTo('password', message='Passwords must match')])
	submit = SubmitField("Register")