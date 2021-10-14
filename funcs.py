import os, datetime
from flask import render_template, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from dotenv import load_dotenv
from db_models import Order, Ordered_item, db, User, Item


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

def fulfill_order(session):
	""" Fulfils order on successful payment """

	uid = session['client_reference_id']
	order = Order(uid=uid, order_date=datetime.datetime.now())
	db.session.add(order)
	db.session.commit()

	current_user = User.query.get(uid)
	for item in current_user.cart_items:
		ordered_item = Ordered_item(oid=order.id, itemid=item.id)
		db.session.add(ordered_item)
		db.session.commit()
		item.owners.remove(current_user)
		db.session.commit()
		print("added order and emptied cart")
		