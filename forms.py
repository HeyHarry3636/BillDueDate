from wtforms import Form, validators, PasswordField, StringField, BooleanField, SelectField, DateField
from wtforms.fields.html5 import EmailField, DecimalField, DateField

class RegisterForm(Form):
	email = EmailField('Email', [
		validators.InputRequired(),
		validators.Email(message='Please enter a valid email address')
	])
	password = PasswordField('Password', [
		validators.InputRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password', [
		validators.InputRequired()
	])
