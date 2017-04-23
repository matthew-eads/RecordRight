from __future__ import print_function
from app import app
from flask import render_template, redirect, request, flash, url_for
from .forms import *
from wtforms import Form, validators
from app.models import Patient
from database import session
import database
import logging
import datetime

from requests_futures.sessions import FuturesSession
from requests.auth import HTTPBasicAuth


import sys

#RRSMS_URL = "http://record-right.herokuapp.com"
RRSMS_URL = "http://localhost:5001"

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	patients = Patient.query.all()
	form = SearchForm(request.form)
	if form.validate() and request.method == 'POST':
		patients = Patient.search_query(form.keyword.data)
		
	return render_template('index.html', patients=patients, form = form)

@app.route('/patient_data/<path:id>', methods=['GET', 'POST'])
def patient_data(id):
	# this converts the patient variable, which is a string, into a dict
	patient = session.query(Patient).filter(Patient.id == id).all()
        print("past visit notes:" )
        print(patient[0].past_visit_notes)
	return render_template('patient_data.html', patient=patient)


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
                form.visit_date.data = str(datetime.date.today())
	if form.validate() and request.method == 'POST':
		patient.name = form.name.data
		patient.DOB = form.DOB.data
		patient.hx = form.hx.data
		patient.phone_number = form.phone_number.data
                if form.visit_notes.data is not None:
                        print("adding visit notes")
                        if patient.past_visit_notes is None:
                                patient.past_visit_notes = {}
                        patient.past_visit_notes[form.visit_date.data] = form.visit_notes.data
                else:
                        print("not adding visit notes")
		database.session.commit()

		request_session = FuturesSession()

		data = {"rr_id":str(id), "name":patient.name, "birth_year":"1970", "birth_month":"01",
			"birth_day":"01", "phone_number":patient.phone_number,
			"address":"None"}
                if form.visit_notes.data is not None:
                        data["notes"] = form.visit_notes.data

		request_session.post("{}/update".format(RRSMS_URL), params=data, 
				     auth=HTTPBasicAuth("admin", "pickabetterpassword"))
		
		return redirect(url_for('patient_data', id=id))
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
	if form.validate() and request.method == 'POST':
                notes = {}
                if form.visit_notes.data is not None and form.visit_date.data is not None:
                        notes[form.visit_date.data] = form.visit_notes.data
		new_patient = Patient(name = form.name.data, DOB = form.DOB.data, 
                                      hx = form.hx.data, phone_number=form.phone_number.data,
                                      past_visit_notes = notes)
		database.session.add(new_patient)
		database.session.commit()
		if form.phone_number.data is not None:
			request_session = FuturesSession()
			data = {"name":form.name.data, "birth_year":"1970", "birth_month":"01",
				"birth_day":"01", "phone_number":form.phone_number.data,
				"address":"None", "notes":form.vist_notes.data, "rr_id":str(new_patient.id)}

			request_session.post("{}/add".format(RRSMS_URL), params=data, 
					     auth=HTTPBasicAuth("admin", "pickabetterpassword"))

		return redirect('/index')
	return render_template('new_patient.html', title="CreatePatient", form=form)

@app.route('/results', methods =['GET', 'POST'])
def show_results():
	return render_template('results.html', results=results)




