from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, FileField, FloatField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Role, Restaurant, FoodItem

class RestaurantForm(Form):
	name 		= StringField('restaurantName')
	description = TextAreaField('description')
	city		= StringField('city')
	submit 		= SubmitField('submit')


class FoodItemForm(Form):
	price 		= FloatField('price')
	#image 		= FileField('image file')
	name 		= StringField('food name')
	description = TextAreaField('description')
	submit 		= SubmitField('submit')
