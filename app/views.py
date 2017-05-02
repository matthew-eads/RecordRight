from __future__ import print_function
from app import app
from flask import render_template, redirect, request, flash, url_for
from .forms import *
from wtforms import Form, validators
from app.models import Patient, Announcement, Reminder, User
from database import session
import database
import logging
import datetime, time
from config import basedir 
import subprocess 
import sqlite3
import re
from requests_futures.sessions import FuturesSession
from requests.auth import HTTPBasicAuth
from functools import wraps

import sys

RRSMS_URL = "http://record-right.herokuapp.com"
# RRSMS_URL = "http://localhost:5001"

# used for page navigation (like going back to search results from Patient Data page)
recent_searches = {}
search_id = 0
curr_user = None
is_admin = False


# defines a decorator for other functions -- requires a user to be logged in
# NOTE: we must add the decorator @login_required to all routes
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if curr_user is None:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	sys.stderr.write("FORM IS validated? %s \n" % form.validate())
	if form.validate() and request.method == 'POST':
		# flash('Login requested for patient=%s, is_remembered=%s' % (form.username.data, str(form.is_remembered.data)))
		given_username = form.username.data
		given_password = form.password.data
		users =	 session.query(User).filter(User.username == given_username).all()
		if users:
			if users[0].password == given_password:
				sys.stderr.write("users are %r\n" % users)
				global curr_user
				curr_user = given_username
				global is_admin
				is_admin = users[0].is_admin
				return redirect('/index')
			else:
				flash("That password is not valid. Please try again.")
		else:
			flash("That username is not valid. Please try again.")
	return render_template('login.html', title="SignIn", form=form, is_admin=is_admin)

@app.route('/logout')
def logout():
	global curr_user
	curr_user = None
	return redirect(url_for('login'))

@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
	announcements = reversed(database.session.query(Announcement).all())
	form = SearchForm(request.form)
	if form.validate() and request.method == 'POST':
		search_id = generate_search_results(form)
		return redirect(url_for('results', search_id=search_id))
	return render_template('index.html', announcements=announcements, form = form, is_admin=is_admin)

@app.route('/view_users')
@login_required
def view_users():
    users = session.query(User).all()
    return render_template('view_users.html', users=users, is_admin=is_admin)

@app.route('/create_user', methods = ['GET', 'POST'])
@login_required
def create_user():
    form = NewUserForm(request.form)
    sys.stderr.write("FORM IS validated? %s \n" % form.validate())
    if form.validate() and request.method == 'POST':
        flash("Successfully created user {}".format(form.username.data))
        users =  session.query(User).filter(User.username == form.username.data).all()
        if users:
            flash("Username {} already exists; please choose a different username".format(form.username.data))
        else:
            new_user = User(username=form.username.data, password=form.password.data, is_admin=form.is_admin.data)
            session.add(new_user)
            session.commit()
            return redirect('index')
    else:
        flash("Limit entries to 3-8 characters")
    return render_template('create_user.html', form=form, is_admin=is_admin)

def generate_search_results(form):
	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	connection = sqlite3.connect('app.db')
	connection.row_factory = dict_factory
	cursor = connection.cursor()
	query = '%' + form.keyword.data + '%'

	cursor.execute("SELECT * FROM patients WHERE hx LIKE ? OR DOB LIKE ? OR name LIKE ? OR phone_number LIKE ? OR address LIKE ?", (query, query, query, query, query,))

	patient_dicts = []

	patient_dicts = cursor.fetchall()

	patients = []

	for p in patient_dicts:
		current = Patient(name = p['name'], DOB = p['DOB'], id = p['id'], hx = p['hx'], phone_number = p['phone_number'], address = p['address'])
		patients.append(current)

		patients.sort(key=lambda p: p.name.split()[-1])
	connection.commit()

	search_data = [patients, form.keyword.data, form]
	global recent_searches
	global search_id
	search_id += 1
	recent_searches[search_id] = search_data
	return search_id  


@app.route('/patient_data/<path:id>/<path:search_id>', methods=['GET', 'POST'])
@login_required
def patient_data(id, search_id):
	# this converts the patient variable, which is a string, into a dict
	patient = session.query(Patient).filter(Patient.id == id).all()
	# i hate everything
	visit_notes = patient[0].past_visit_notes
	# maybe a better way to do this... but this'll work for now
	# keep the visit notes sorted based on date
	if visit_notes is None:
		sorted_notes = None
	else:
		try:
			sorted_notes = reversed(sorted(visit_notes.iteritems(), 
								  key=lambda datestr: time.strptime(datestr[0], "%m/%d/%Y")))
		except:
			sorted_notes = list(visit_notes.iteritems())
	return render_template('patient_data.html', patient=patient, visit_notes=sorted_notes, search_id=search_id, is_admin=is_admin)

# if new=True, send to /add, else send to /update
def send_update_to_sms_server(patient, new=False):
	request_session = FuturesSession()
	date = datetime.datetime.strptime(patient.DOB, "%m/%d/%Y")
	data = {"rr_id":str(id), "name":patient.name, "birth_year":str(date.year), 
			"birth_month":str(date.month), "birth_day":str(date.day), 
			"phone_number":patient.phone_number, "address":patient.address, "notes":patient.patient_note}
	path = "add" if new else "update"
	request_session.post("{}/{}".format(RRSMS_URL, path), params=data, auth=HTTPBasicAuth("admin", "pickabetterpassword"))

						
def prepopulate_form(form, patient):
	form.name.data = patient.name
	form.DOB.data = patient.DOB
	form.hx.data = patient.hx
	form.phone_number.data = patient.phone_number
	form.address.data = patient.address
	today = datetime.date.today().strftime("%m/%d/%Y")
	form.visit_date.data = today
	form.patient_note.data = patient.patient_note

@app.route('/update_patient_data/<path:id>/<path:search_id>', methods=['GET', 'POST'])
@login_required
def update_patient_data(id, search_id):
	# this converts the patient variable, which is a string, into a dict
	#import pdb; pdb.set_trace()
	patients = session.query(Patient).filter(Patient.id == id).all()
	patient = patients[0]
	form = NewPatientForm(request.form)
	if request.method == "GET":
		prepopulate_form(form, patient)
	if form.validate() and request.method == 'POST':
		patient.name = form.name.data
		patient.DOB = clean_date(form.DOB.data)
		patient.hx = form.hx.data
		patient.phone_number = form.phone_number.data
		patient.address = form.address.data
		patient.patient_note = form.patient_note.data

		if form.visit_notes.data is not None and form.visit_notes.data != "":
			if patient.past_visit_notes is None:
				patient.past_visit_notes = {}
			#patient.past_visit_notes[form.visit_date.data] = form.visit_notes.data
			notes_info = []
			notes_info.append(form.visit_doctor.data)
			notes_info.append(form.visit_notes.data)
			patient.past_visit_notes[form.visit_date.data] = notes_info

		database.session.commit()
		send_update_to_sms_server(patient)
		flash("Successfully updated patient {}".format(form.name.data))
		return redirect(url_for('patient_data', id=id, search_id=search_id))
	elif request.method == 'POST':
		flash_errors(form)
	return render_template('update_patient_data.html', patient=patient, form=form, search_id=search_id, is_admin=is_admin)


@app.route('/new_visit/<path:id>/<path:search_id>', methods=['GET', 'POST'])
@login_required
def new_visit(id, search_id):
	patients = session.query(Patient).filter(Patient.id == id).all()
	patient = patients[0]
	form = NewVisitForm(request.form)
	if request.method == "GET":
		today = datetime.date.today().strftime("%m/%d/%Y")
		form.visit_date.data = today
		form.patient_note.data = patient.patient_note
	if form.validate() and request.method == 'POST':
		patient.patient_note = form.patient_note.data

		if form.visit_notes.data is not None and form.visit_notes.data != "":
			if patient.past_visit_notes is None:
				patient.past_visit_notes = {}
			notes_info = []
			notes_info.append(form.visit_doctor.data)
			notes_info.append(form.visit_notes.data)
			patient.past_visit_notes[form.visit_date.data] = notes_info

		database.session.commit()
		send_update_to_sms_server(patient)
		return redirect(url_for('patient_data', id=id, search_id=search_id))
	return render_template('new_visit.html', patient=patient, form=form, search_id=search_id, is_admin=is_admin)	   

@app.route('/new_patient', methods=['GET', 'POST'])
@login_required
def create_patient():
	form = NewPatientForm(request.form)
	if request.method == 'GET':
		today = datetime.date.today().strftime("%m/%d/%Y")
		form.visit_date.data = today
	if form.validate() and request.method == 'POST':
		notes = {}
		if form.visit_notes.data is not None and form.visit_notes.data != "":
			notes[form.visit_date.data] = form.visit_notes.data
		new_patient = Patient(name = form.name.data, DOB = clean_date(form.DOB.data), 
							  hx = form.hx.data, phone_number=form.phone_number.data,
							  past_visit_notes = notes, address=form.address.data, patient_note=form.patient_note.data)
		database.session.add(new_patient)
		database.session.commit()
		if form.phone_number.data is not None:
			send_update_to_sms_server(new_patient, new=True)
		flash("Successfully added patient {}".format(form.name.data))
		return redirect('/index')
	elif request.method == 'POST':
		flash_errors(form)
	return render_template('new_patient.html', title="CreatePatient", form=form, is_admin=is_admin)


@app.route('/delete_patient/<path:id>')
@login_required
def delete_patient(id):
	patient = session.query(Patient).filter(Patient.id == id).all()
	name = patient[0].name
	session.query(Patient).filter(Patient.id == id).delete()
	database.session.commit()
	flash("Successfully deleted patient {}".format(name))
	return redirect(url_for('index'))

def clean_date(date):
	(month, day, year) = date.split('/')
	if len(month) == 1:
		month = "0{}".format(month)
	if len(day) == 1:
		day = "0{}".format(day)
	if len(year) == 2:
		prefix = "19" if int(year) > (datetime.date.today().year - 2000) else "20"
		year = "{}{}".format(prefix, year)
	return "{}/{}/{}".format(month,day,year)

def handle_single_form(single_form, patient):
	# schedule reminder
	body = single_form.what.data
	to_number = patient.phone_number
	date = single_form.when.data
	command = "{}/RRSMS/send_reminder.bash -n {} -m \"{}\"".format(basedir, to_number, body)
	proc = subprocess.Popen(['at', date], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.stdin.write(command)
	proc.stdin.close()
	out = proc.stdout.read()
	flash("Successfully set reminder for {}".format(patient.name))
	reminder = Reminder()
	reminder.reminder_type = 1
	reminder.patient_id = patient.id
	reminder.schedule = date
	reminder.message = body
	reminder.at_id = int(re.search('job ([0-9]+)', out).groups()[0])
	database.session.add(reminder)
	database.session.commit()

def handle_recurrent_form(recurrent_form, common_reminder_form, patient, search_id):
	print("Creating recurrent reminder")
	is_common_selected = common_reminder_form.validate()
	f = common_reminder_form if is_common_selected else recurrent_form
	body = f.what.data
	to_number = patient.phone_number
				
	if (f.end_after.data is None or f.end_after.data == "") and (
		f.end_on.data is None or f.end_after.data == ""):
		flash("Error: please specify either the 'end after' field or the 'end on' field")
		return render_template("create_reminder.html", patient=patient, single_form=single_form, recurrent_form=recurrent_form,
							   common_reminder_form=common_reminder_form, search_id=search_id, is_admin=is_admin)
	reminder = Reminder()
	reminder.reminder_type = 2
	reminder.message = body
	reminder.patient_id = patient.id
		
	if is_common_selected:
		schedule = f.schedule.data
	else:
		start_hour = "0" if f.start_hour.data is None or f.start_hour.data == '' else f.start_hour.data 
		end_hour = "23" if f.end_hour.data is None or f.end_hour.data == '' else f.end_hour.data 
		schedule = "0 {}-{}/{} */{} * *".format(
			start_hour, end_hour, f.hours.data, f.days.data)
	reminder.schedule = schedule
	# ok so for the end_after x occurrences, not quite sure what the best way is
	# best i got right now is just shove a counter in the file
	run_script = ""
	if f.end_after.data is not None and f.end_after.data != '':
		reminder.end_after = int(f.end_after.data)
		counter_name = "{}/.scheduling/{}-{}.count".format(basedir, to_number, str(time.time()))
		script_name = "{}/.scheduling/{}-{}.bash".format(basedir, to_number, str(time.time()))
		script = """
		#!/bin/bash
		fname="{}"
		count=`cat $fname`
		count=$((count-1))
		if [ $count -lt 1 ]; then
		# time to die
		echo "killing self"
		crontab -l | grep -Fv \"{}\" | crontab -
		rm $fname
		rm {}
		exit 0
		fi
		echo "not dead yet... decrementing counter"
		echo $count > $fname\n""".format(counter_name, script_name, script_name)
		run_script = "; bash {}".format(script_name)
		script_f = open(script_name, "w+")
		script_f.write(script)
		script_f.close()
		counter_f = open(counter_name, "w+")
		counter_f.write("{}\n".format(f.end_after.data))
		counter_f.close()

		subcommand = "{} {}/RRSMS/send_reminder.bash -n {} -m \\\"{}\\\"{}".format(
			schedule, basedir, to_number, body, run_script)
		reminder.cron_command = subcommand
		command = "(crontab -l; echo \"{}\") | crontab - ".format(subcommand)
		print("command is: {}".format(command))
		proc = subprocess.Popen(["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		proc.stdin.write(command)
		proc.stdin.close()
		print(proc.stdout.read())

	if f.end_on.data is not None and f.end_on.data != '':
		reminder.end_on = f.end_on.data
		proc = subprocess.Popen(["at", f.end_on.data], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		proc.stdin.write("crontab -l\n")
		proc.stdin.write("crontab -l | grep -Fv \"{}\" | crontab - ".format(subcommand))
		proc.stdin.close()
		print("Output: {}".format(proc.stdout.read()))
	database.session.add(reminder)
	database.session.commit()
	flash("Successfully set reminder for {}".format(patient.name))
	return redirect(url_for('patient_data', id=patient.id, search_id=search_id))

@app.route('/create_reminder/<path:id>/<path:search_id>', methods=['GET', 'POST'])
@login_required
def create_reminder(id, search_id):
	patient = session.query(Patient).filter(Patient.id == id).first()
	if patient.phone_number is None:
		# can't send a reminder without a number
		flash("There is no phone number recorded for {}. Please update their record with their phone number to send them reminders".format(patient.name))
		return redirect(url_for('patient_data', id=id, search_id=search_id))			
	single_form = ReminderForm(request.form)
	recurrent_form = RecurrentReminderForm(request.form)
	common_reminder_form = CommonReminderForm(request.form)
	if request.method == 'GET':
		recurrent_form.start_hour.data = "00"
		recurrent_form.end_hour.data = "23"

	if single_form.validate() and request.method == 'POST':
		handle_single_form(single_form, patient)
		return redirect(url_for('patient_data', id=id, search_id=search_id))
		
	if (recurrent_form.validate() or common_reminder_form.validate()) and request.method == 'POST':
		return handle_recurrent_form(recurrent_form, common_reminder_form, patient, search_id)


	if request.method == 'POST':
		form_name = request.form['form-name']
		if form_name == "singleform":
			flash_errors(single_form)
		elif form_name == "recurrentreminderform":
			flash_errors(recurrent_form)
		else:
			flash_errors(common_reminder_form)
		
	return render_template("create_reminder.html", patient=patient, single_form=single_form, recurrent_form=recurrent_form,
						   common_reminder_form=common_reminder_form, search_id=search_id, is_admin=is_admin)

@app.route('/results/<path:search_id>', methods=['GET', 'POST'])
@login_required
def results(search_id):
	form = SearchForm(request.form)
	if form.validate() and request.method == 'POST':
		search_id = generate_search_results(form)
		# return render_template('results.html', patients=patients, form = form, query = form.keyword.data)
		return redirect(url_for('results', search_id=search_id))

	global recent_searches
	search_id = int(search_id)
	search = recent_searches[search_id]

	patients = search[0]
	query = search[1]
	form = search[2]

	return render_template('results.html', patients=patients, form=form, query=query, search_id=search_id, is_admin=is_admin)

@app.route('/newannouncement', methods =['GET', 'POST'])
@login_required
def create_announcement():
	form = NewAnnouncementForm(request.form)
	if form.validate() and request.method == 'POST':
		if form.announcement.data is not None and form.name.data is not None and form.severity.data is not None:
			today = datetime.date.today().strftime("%m/%d/%Y")
			new_announcement = Announcement(name = form.name.data, announcement = form.announcement.data, date = today, severity = form.severity.data)
			database.session.add(new_announcement)
			database.session.commit()
			return redirect('/index')
	return render_template('new_announcement.html', form = form, is_admin=is_admin)

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			fieldname = getattr(form, field).label.text
			if fieldname == "what":
				fieldname = "message"
			if fieldname == "when":
				fieldname = "date to send"
			flash(u"Error in the %s field - %s" % (fieldname, error))
