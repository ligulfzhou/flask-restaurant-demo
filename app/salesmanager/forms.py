from flask.ext.wtf import Form
from wtform import StringField, TextAreaField, SubmitField, FileField, FloatField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role, Restaurant, FoodItem

class RestaurantForm(Form):
	name 		= StringField('restaurantName')
	description = TextField('description')
	city		= StringField('city')
	submit 		= SubmitField('submit')


class FoodItem(Form):
	price 		= FloatField('price')
	image 		= FileField('image file')
	name 		= StringField('food name')
	description = TextAreaField('description')
