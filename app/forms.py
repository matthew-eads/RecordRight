# forms.py
from wtforms import Form, BooleanField, StringField, validators, IntegerField, HiddenField, SelectField

class LoginForm(Form):
	username = StringField('username', [validators.DataRequired()])
	is_remembered = BooleanField('is_remembered', default=False)

class NewPatientForm(Form):
	name = StringField('name', [validators.DataRequired()])
	DOB = StringField('DOB', [validators.DataRequired()])
	hx = StringField('hx', [])
	phone_number = StringField('phone_number', [])
        address = StringField('address', [])
        visit_date = StringField("visit_date", [])
        visit_notes = StringField("visit_notes", [])

class SearchForm(Form):
	#name = StringField('name')
	#DOB = StringField('DOB')
	keyword = StringField('keyword')

class CommonReminderForm(Form):
        what = HiddenField('what', [validators.DataRequired()])
        schedule = SelectField('Reminder Schedule', choices=[('0 6 * * *', "Once daily at 6am"), ('0 6,12,18 * * *', "Thrice daily at 6am, noon, and 6pm")])
        end_after = StringField('end_after')
        end_on = StringField('end_on')

class ReminderForm(Form):
        what = HiddenField('message', [validators.DataRequired()])
        when = StringField('when', [validators.DataRequired()])

class RecurrentReminderForm(Form):
        what = HiddenField('message', [validators.DataRequired()])
        days = IntegerField('days', [validators.DataRequired()])
        hours = IntegerField('hours', [validators.DataRequired()])
        start_hour = IntegerField('start_hour')
        end_hour = StringField('end_hour')
        end_after = StringField('end_after')
        end_on = StringField('end_on')
