from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, RadioField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    city = StringField('city', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class SearchRestaurantByCity(Form):
    city        = StringField('city', validators=[Required()])
    submit      = SubmitField('search')
