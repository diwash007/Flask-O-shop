from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

cart = db.Table('cart',
		db.Column('uid', db.Integer, db.ForeignKey('users.id')),
		db.Column('itemid', db.Integer, db.ForeignKey('items.id'))
)

class User(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	email = db.Column(db.String(50), nullable=False)
	phone = db.Column(db.String(50), nullable=False)
	password = db.Column(db.String(250), nullable=False)
	admin = db.Column(db.Boolean, nullable=True, default=False)
	email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
	cart_items = db.relationship("Item", secondary=cart, backref=db.backref('owners', lazy='dynamic'))

class Item(db.Model):
	__tablename__ = "items"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	price = db.Column(db.Float, nullable=False)
	category = db.Column(db.Text, nullable=False)
	image = db.Column(db.String(250), nullable=False)
	details = db.Column(db.String(250), nullable=False)
	price_id = db.Column(db.String(250), nullable=False)
# 	user = relationship("Cart", back_populates="item")

# class Cart(db.Model):
# 	__tablename__ = "cart"
# 	id = db.Column(db.Integer, primary_key=True)
# 	uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# 	itemid = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
# 	user = relationship("User", back_populates="item")
# 	item = relationship("Item", back_populates="user")