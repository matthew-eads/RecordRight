# forms.py
from wtforms import Form, BooleanField, StringField, validators, IntegerField

class LoginForm(Form):
	username = StringField('username', [validators.DataRequired()])
	is_remembered = BooleanField('is_remembered', default=False)

class NewPatientForm(Form):
	name = StringField('name', [validators.DataRequired()])
	DOB = StringField('DOB', [validators.DataRequired()])
	hx = StringField('hx', [validators.DataRequired()])
	phone_number = StringField('phone_number', [])
        visit_date = StringField("visit_date", [])
        visit_notes = StringField("visit_notes", [])

class SearchForm(Form):
	#name = StringField('name')
	#DOB = StringField('DOB')
	keyword = StringField('keyword')

class ReminderForm(Form):
        when = StringField('when', [validators.DataRequired()])
        what = StringField('what', [validators.DataRequired()])

class RecurrentReminderForm(Form):
        what = StringField('what', [validators.DataRequired()])
        days = IntegerField('days', [validators.DataRequired()])
        hours = IntegerField('hours', [validators.DataRequired()])
        start_hour = IntegerField('start_hour')
        end_hour = StringField('end_hour')
        end_after = StringField('end_after')
        end_on = StringField('end_on')
