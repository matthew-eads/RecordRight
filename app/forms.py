# forms.py
from wtforms import Form, BooleanField, StringField, validators, IntegerField, TextAreaField
from wtforms import HiddenField, SelectField, RadioField, PasswordField


class LoginForm(Form):
	username = StringField('username', [validators.DataRequired()])
	password = PasswordField('password', [validators.DataRequired()])
	is_remembered = BooleanField('is_remembered', default=False)



class NewPatientForm(Form):
    name = StringField('name', [validators.DataRequired()])
    DOB = StringField('DOB', [validators.DataRequired()])
    hx = StringField('hx', [])
    phone_number = StringField('phone_number', [])
    address = StringField('address', [])
    visit_date = StringField("visit_date", [])
    visit_doctor = StringField("visit_doctor", [])
    visit_notes = TextAreaField("visit_notes", render_kw={"rows": 3, "cols": 40})
    patient_note = StringField("patient_note", [])

class NewVisitForm(Form):
    visit_date = StringField('visit_date', [])
    visit_doctor = StringField('visit_doctor', [])
    visit_notes = TextAreaField("visit_notes", render_kw={"rows": 3, "cols": 40})
    patient_note = StringField("patient_note", [])


class SearchForm(Form):
	keyword = StringField('keyword')

class NewUserForm(Form):
        username= StringField('username', [validators.DataRequired(), validators.Length(3,8,"Please enter a value between 3 and 8 characters")])
        password = StringField('password', [validators.DataRequired(), validators.Length(3,8,"Please enter a value between 3 and 8 characters")])
        is_admin= BooleanField('is_admin', default=False)

class CommonReminderForm(Form):
	what = HiddenField('what', [validators.DataRequired()])
	schedule = SelectField('Reminder Schedule', 
                               choices=[('0 6 * * *', "Once daily at 6am"), 
                                        ('0 6,12,18 * * *', "Thrice daily at 6am, noon, and 6pm"),
                                        ('0 6,18 * * *', "Twice a day at 6am and 6pm")])
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

class NewAnnouncementForm(Form):
	name = StringField('name', [validators.DataRequired()])
	announcement = StringField('announcement', [validators.DataRequired()])
	severity = RadioField('Severity', choices=[('Low','Low'),('Medium','Medium'),('High', 'High')])
