from __future__ import print_function
from app import app
from flask import render_template, redirect, request, flash, url_for
from .forms import *
from wtforms import Form, validators
from app.models import Patient
from database import session
import database
import logging
import datetime, time
from config import basedir 
import subprocess 

from requests_futures.sessions import FuturesSession
from requests.auth import HTTPBasicAuth


import sys

RRSMS_URL = "http://record-right.herokuapp.com"
# RRSMS_URL = "http://localhost:5001"


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    patients = database.session.query(Patient).all()
    form = SearchForm(request.form)
    if form.validate() and request.method == 'POST':
		patients = Patient.search_query(form.keyword.data)
    return render_template('index.html', patients=patients, form = form)

@app.route('/patient_data/<path:id>', methods=['GET', 'POST'])
def patient_data(id):
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
                        sorted_notes = sorted(visit_notes.iteritems(), 
                                              key=lambda datestr: time.strptime(datestr[0], "%m/%d/%Y"))
                except:
                        sorted_notes = list(visit_notes.iteritems())
                        

	return render_template('patient_data.html', patient=patient, visit_notes=sorted_notes)


@app.route('/update_patient_data/<path:id>', methods=['GET', 'POST'])
def update_patient_data(id):
	# this converts the patient variable, which is a string, into a dict
	#import pdb; pdb.set_trace()
	patients = session.query(Patient).filter(Patient.id == id).all()
	patient = patients[0]
	form = NewPatientForm(request.form)
	if request.method == "GET":
		form.name.data = patient.name
		form.DOB.data = patient.DOB
		form.hx.data = patient.hx
                form.phone_number.data = patient.phone_number
                form.address.data = patient.address
                today = datetime.date.today().strftime("%m/%d/%Y")
                form.visit_date.data = today
	if form.validate() and request.method == 'POST':
		patient.name = form.name.data
		patient.DOB = form.DOB.data
		patient.hx = form.hx.data
		patient.phone_number = form.phone_number.data
                patient.address = form.address.data
                if form.visit_notes.data is not None:
                        print("adding visit notes")
                        if patient.past_visit_notes is None:
                                patient.past_visit_notes = {}
                        patient.past_visit_notes[form.visit_date.data] = form.visit_notes.data
                        
                        #TODO remove this... this is just for fixing date inconsistencies
                        for datestr in patient.past_visit_notes.keys():
                                try:
                                        datetime.datetime.strptime(datestr, "%m/%d/%Y")
                                except ValueError:
                                        date = datetime.datetime.strptime(datestr, "%Y-%m-%d")
                                        patient.past_visit_notes[date.strftime("%m/%d/%Y")] = patient.past_visit_notes[datestr]
                                        del patient.past_visit_notes[datestr]
                else:
                        print("not adding visit notes")
		database.session.commit()

		request_session = FuturesSession()
                date = datetime.datetime.strptime(datestr, "%m/%d/%Y")
		data = {"rr_id":str(id), "name":patient.name, "birth_year":str(date.year), "birth_month":str(date.month),
			"birth_day":str(date.day), "phone_number":patient.phone_number,
			"address":"None"}
                if form.visit_notes.data is not None:
                        data["notes"] = form.visit_notes.data

		request_session.post("{}/update".format(RRSMS_URL), params=data, 
				     auth=HTTPBasicAuth("admin", "pickabetterpassword"))
                flash("Successfully updated patient {}".format(form.name.data))
		return redirect(url_for('patient_data', id=id))
        elif request.method == 'POST':
                flash_errors(form)
	return render_template('update_patient_data.html', patient=patient, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	sys.stderr.write("FORM IS validated? %s \n" % form.validate())
	if form.validate() and request.method == 'POST':
		# flash('Login requested for patient=%s, is_remembered=%s' % (form.username.data, str(form.is_remembered.data)))
		return redirect('/index')
	return render_template('login.html', title="SignIn", form=form)

@app.route('/new_patient', methods=['GET', 'POST'])
def create_patient():
	form = NewPatientForm(request.form)
        if request.method == 'GET':
                today = datetime.date.today().strftime("%m/%d/%Y")
                form.visit_date.data = today
	if form.validate() and request.method == 'POST':
                notes = {}
                if form.visit_notes.data is not None and form.visit_date.data is not None:
                        notes[form.visit_date.data] = form.visit_notes.data
		new_patient = Patient(name = form.name.data, DOB = form.DOB.data, 
                                      hx = form.hx.data, phone_number=form.phone_number.data,
                                      past_visit_notes = notes, address=form.address.data)
		database.session.add(new_patient)
		database.session.commit()
		if form.phone_number.data is not None:
			request_session = FuturesSession()
                        date = datetime.datetime.strptime(form.DOB.data, "%m/%d/%Y")
			data = {"name":form.name.data, "birth_year":str(date.year), "birth_month":str(date.month),
				"birth_day":str(date.day), "phone_number":form.phone_number.data,
				"address":form.address.data, "notes":form.visit_notes.data, "rr_id":str(new_patient.id)}

			request_session.post("{}/add".format(RRSMS_URL), params=data, 
					     auth=HTTPBasicAuth("admin", "pickabetterpassword"))
                flash("Successfully added patient {}".format(form.name.data))
		return redirect('/index')
        elif request.method == 'POST':
                flash_errors(form)
	return render_template('new_patient.html', title="CreatePatient", form=form)

@app.route('/create_reminder/<path:id>', methods=['GET', 'POST'])
def create_reminder(id):
        patient = session.query(Patient).filter(Patient.id == id).first()
        if patient.phone_number is None:
            # can't send a reminder without a number
            flash("There is no phone number recorded for {}. Please update their record with their phone number to send them reminders".format(patient.name))
            return redirect(url_for('patient_data', id=id))            
        single_form = ReminderForm(request.form)
        recurrent_form = RecurrentReminderForm(request.form)
        common_reminder_form = CommonReminderForm(request.form)
        if single_form.validate() and request.method == 'POST':
                # schedule reminder
                body = single_form.what.data
                to_number = patient.phone_number
                date = single_form.when.data
                command = "{}/RRSMS/send_reminder.bash -n {} -m \"{}\"".format(basedir, to_number, body)
                proc = subprocess.Popen(['at', date], stdin=subprocess.PIPE)
                proc.stdin.write(command)
                proc.stdin.close()
                flash("Successfully set reminder for {}".format(patient.name))
                return redirect(url_for('patient_data', id=id))
        
        if (recurrent_form.validate() or common_reminder_form.validate()) and request.method == 'POST':
                print("Creating recurrent reminder")
                is_common_selected = common_reminder_form.validate()
                f = common_reminder_form if is_common_selected else recurrent_form
                body = f.what.data
                to_number = patient.phone_number
                
                if (f.end_after.data is None or f.end_after.data == "") and (
                    f.end_on.data is None or f.end_after.data == ""):
                        flash("Error: please specify either the 'end after' field or the 'end on' field")
                        return render_template("create_reminder.html", patient=patient, single_form=single_form, recurrent_form=recurrent_form,
                                               common_reminder_form=common_reminder_form)
        

                if is_common_selected:
                        schedule = f.schedule.data
                else:
                        schedule = "0 {}-{}/{} */{} * *".format(
                                f.start_hour.data, f.end_hour.data, f.hours.data, f.days.data)
                
                # ok so for the end_after x occurrences, not quite sure what the best way is
                # best i got right now is just shove a counter in the file
                run_script = ""
                if f.end_after.data is not None:
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

                command = "(crontab -l; echo \"{}\") | crontab - ".format(subcommand)
                print("command is: {}".format(command))
                proc = subprocess.Popen(["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                proc.stdin.write(command)
                proc.stdin.close()
                print(proc.stdout.read())
                #import pdb; pdb.set_trace()
                #TODO: make sure we actually ~~STOP~~ sending messages based on either end_after or end_on
                if f.end_on.data is not None and f.end_on.data != '':
                        proc = subprocess.Popen(["at", f.end_on.data], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                        proc.stdin.write("crontab -l\n")
                        print("grepping for \"{}\"".format(subcommand))
                        proc.stdin.write("crontab -l | grep -Fv \"{}\" | crontab - ".format(subcommand))
                        proc.stdin.close()
                        print("Output: {}".format(proc.stdout.read()))
                        
                flash("Successfully set reminder for {}".format(patient.name))
                return redirect(url_for('patient_data', id=id))

        if request.method == 'POST':
                form_name = request.form['form-name']
                if form_name == "singleform":
                        flash_errors(single_form)
                elif form_name == "recurrentreminderform":
                        flash_errors(recurrent_form)
                else:
                        flash_errors(common_reminder_form)
        
        return render_template("create_reminder.html", patient=patient, single_form=single_form, recurrent_form=recurrent_form,
                               common_reminder_form=common_reminder_form)
        

@app.route('/results', methods =['GET', 'POST'])
def show_results():
	return render_template('results.html', results=results)

  



def flash_errors(form):
        for field, errors in form.errors.items():
                for error in errors:
                        fieldname = getattr(form, field).label.text
                        if fieldname == "what":
                                fieldname = "message"
                        if fieldname == "when":
                                fieldname = "date to send"
                        flash(u"Error in the %s field - %s" % (fieldname, error))
