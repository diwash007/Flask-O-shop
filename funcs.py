import os
from flask import render_template, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from dotenv import load_dotenv


load_dotenv()
mail = Mail()

def send_confirmation_email(user_email) -> None:
	""" sends confirmation email """
	confirm_serializer = URLSafeTimedSerializer(os.environ["SECRET_KEY"])
	confirm_url = url_for(
						'confirm_email',
						token=confirm_serializer.dumps(user_email,
						salt='email-confirmation-salt'),
						_external=True)
	html = render_template('email_confirmation.html', confirm_url=confirm_url)
	msg = Message(
		'Confirm Your Email Address',
		recipients=[user_email],
		html=html,
		sender="freequotesforyoumyfriend@gmail.com"
	)
	mail.send(msg)