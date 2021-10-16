from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, FileField
from wtforms.validators import DataRequired, Length


class AddItemForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired(), Length(max=50)])
	price = FloatField("Price:", validators=[DataRequired()])
	category = StringField("Category:", validators=[DataRequired(), Length(max=50)])
	image = FileField("Image:", validators=[DataRequired()])
	details = StringField("Details:", validators=[DataRequired()])
	price_id = StringField("Stripe id:", validators=[DataRequired()])
	submit = SubmitField("Add")

class OrderEditForm(FlaskForm):
	status = StringField("Status:", validators=[DataRequired()])
	submit = SubmitField("Update")