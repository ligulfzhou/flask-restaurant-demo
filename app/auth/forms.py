from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email       = StringField('Email', validators=[Required(), Length(1, 64),
                                                Email()])
    password    = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('keep me logged in')
    submit      = SubmitField('Log in')


class RegistrationForm(Form):
    email   	= StringField('Email', validators=[Required(), Length(1, 64),
    											Email()])
    username 	=  StringField('Username', validators=[
    	Required(), Length(1,64), Regexp(^[A-Za-z][A-Za-z0-9_.]*$, 0,
    										'Username must have only letters,'
    										'numbers, dots or underscores')])
    password 	= PasswordField('Password', validators=[
    	Required(), EqualTo(password2, message='Password must match')])
    password2	= PasswordField('Password', validators=[Required()])
    submit 		= SubmitField('Register')

    def validate_email(self, field):
    	if User.query.filter_by(email=filed.data).first():
    		raise ValidationError('Email already registered')

    def validate_username(self, filed):
    	if User.query.filter_by(username=filed.data).first():
    		raise ValidationError('Username already taken')


class ChangePasswordForm(Form):
	old_password 	= PasswordField('Old password', validators=[Required()])
	password 		= PasswordField('New password', validators=[
		Required(), EqualTo('password2', message='password must match')])
	password2 		= PasswordField('Confirm new password', validators=[Required()])
	submit 			= SubmitField('Update your password')


class PasswordResetRequestForm(Form):
	email 		= StringField('Email', validators=[Required(), Length(1, 64),
													Email()])
	submit 		= SubmitField('Reset password')


class PasswordResetForm(Form):
	email 		= StringField('Email', validators=[Required(), Length(1, 64),
													Email()])
	password 	= PasswordField('New password', validators=[
		Required(), EqualTo('password2', message='password must match')])
	password2 	= PasswordField('Confirm password', validators=[Required()])
	submit 		= SubmitField('Reset password')

	def validate_email(self, field):
		if User.query.filter_by(email=filed.data).first() is None:
			raise ValidationError('Unknown email address')


class ChangeEmailForm(Form):
	email 		= StringField('New email', validators=[Required(), Length(1, 64),
														Email()])
	password 	= StringField('Password', validators=[Required()])
	submit 		= SubmitField('Update Email Address')

	def validate_email(self, field):
		if User.query.filter_by(email=filed.data).first():
			raise ValidationError('Email already taken')