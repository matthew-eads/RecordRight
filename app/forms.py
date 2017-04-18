# forms.py
from wtforms import Form, BooleanField, StringField, validators

class LoginForm(Form):
	username = StringField('username', [validators.DataRequired()])
	is_remembered = BooleanField('is_remembered', default=False)