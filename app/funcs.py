import os, datetime
from flask import render_template, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_login import current_user
from flask_mail import Mail, Message
from dotenv import load_dotenv
from .db_models import Order, Ordered_item, db, User


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
		sender="Flask-O-shop Email confirmation"
	)
	mail.send(msg)

def fulfill_order(session):
	""" Fulfils order on successful payment """

	uid = session['client_reference_id']
	order = Order(uid=uid, date=datetime.datetime.now(), status="processing")
	db.session.add(order)
	db.session.commit()

	current_user = User.query.get(uid)
	for cart in current_user.cart:
		ordered_item = Ordered_item(oid=order.id, itemid=cart.item.id, quantity=cart.quantity)
		db.session.add(ordered_item)
		db.session.commit()
		current_user.remove_from_cart(cart.item.id, cart.quantity)
		db.session.commit()

def admin_only(func):
	""" Decorator for giving access to authorized users only """
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated and current_user.admin == 1:
			return func(*args, **kwargs)
		else:
			return "You are not Authorized to access this URL."
	wrapper.__name__ = func.__name__
	return wrapper
		