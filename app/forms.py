# forms.py
from wtforms import Form, BooleanField, StringField, validators

class LoginForm(Form):
	username = StringField('username', [validators.DataRequired()])
	is_remembered = BooleanField('is_remembered', default=False)

class NewPatientForm(Form):
	name = StringField('name', [validators.DataRequired()])
	DOB = StringField('DOB', [validators.DataRequired()])
	hx = StringField('hx', [validators.DataRequired()])

class SearchForm(Form):
	#name = StringField('name')
	#DOB = StringField('DOB')
	keyword = StringField('keyword')