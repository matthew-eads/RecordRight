from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	users = [ { 'name' : 'Matt Eads', 'DOB' : '04/38/27'}, { 'name' : 'Robert Downey Jr', 'DOB' : '11/27/69'}]
	return render_template('index.html', users=users)

@app.route('/patientdata/<path:user>')
def patient_data(user):
	user = eval(user)
	return render_template('patient_data.html', user=user)

