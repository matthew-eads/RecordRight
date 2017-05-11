import twilio.twiml
from twilio.rest import TwilioRestClient
import sys,os 
import argparse
import datetime
from flask import Flask, request, redirect, session, make_response, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from functools import wraps
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--production', action='store_true')

    args = parser.parse_args(sys.argv[1:])
    production = args.production
    SQLALCHEMY_ECHO = False if production else True

port = int(os.getenv('PORT', '5001'))
ACCOUNT_SID = "ACbaca90abfe93b3a0c75a44d71ed1e0c2"
AUTH_TOKEN = "8b1c193701c6f7332f669d1448ddbc68"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'top secret'
app =  Flask(__name__) 
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
if app.config['SQLALCHEMY_DATABASE_URI'] == None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

import models_test


@app.route('/', methods=["GET", "POST"])
def main():
    
    #print(str(request.data))
    #print(str(request.values))
    print("from: {0}, body {1}".format(request.values.get('From', None), request.values.get('Body', None)))
    print("menu_state: {}".format(request.cookies.get("menu_state", "0")))
    (return_body, menu_state) = process_message(request.values.get('Body', None), 
                                                request.values.get('From', None),
                                                int(request.cookies.get('menu_state', '0')))

    twilio_resp = twilio.twiml.Response()
    twilio_resp.message(return_body)
    resp = make_response(str(twilio_resp))
    resp.set_cookie('menu_state', str(menu_state))
    
    return resp
    
# check_auth, authenticate, requires_auth taken from http://flask.pocoo.org/snippets/8/
# authored by Armin Ronacher
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'pickabetterpassword'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Adds a patient to the db - see add_db.py
@app.route('/add', methods=["GET", "POST"])
@requires_auth
def add_db():
    print("Adding db")
    try:
        p = models_test.Patient(name=request.values.get('name', None),
                                birth_year=int(request.values.get('birth_year', None)),
                                birth_month=int(request.values.get('birth_month', None)),
                                birth_day=int(request.values.get('birth_day', None)),
                                phone_number=clean_number(request.values.get('phone_number', None)),
                                address=request.values.get('address', None),
                                notes=request.values.get('notes', None),
                                rr_id=int(request.values.get('rr_id', None)))
        # TODO: check not duplicate
        db.session.add(p)
        db.session.commit()
        # Send a nice welcome message to the patient
        to_number = clean_number(request.values.get('phone_number', None))
        if to_number is None:
            print("Can't send welcome message; phone_number not given")
            return Response("Updated db, no welcome sent", 200, {})
        else:
            body = ("Welcome to RecordRight! You can text this number to check "
                "information in your record (such as notes from recent visits) "
                "or update personal information. Send any message to begin."
                "Send 'QUIT' at any time to return to the main menu, or 'HELP' for help.")
            client.messages.create(to=to_number, from_="+19182387039", body=body)
            return Response("Successfully updated db", 200, {})
    except Exception as e:
        print("Error updating db: {}".format(e))
        return Response("Error updating db", 200, {})

# Updates an existing patient record in the db - see update_db.py
@app.route('/update', methods=["GET", "POST"])
@requires_auth
def update_db():
    print("Updating db")
    try:
        p_id = request.values['rr_id'] # if this isn't here, then we're out of luck
        
        # we can use first - really should be no way there are duplicate ids
        patient = db.session.query(models_test.Patient).filter(models_test.Patient.rr_id == int(p_id)).first()
        if patient is None:
            print("Couldn't find based on rr_id")
            # generally this shouldn't happen, but life isn't perfect ya know
            # so lets just assume we have a name and no dups
            name = request.values['name']
            patient = db.session.query(models_test.Patient).filter(models_test.Patient.name == name).first()
            if patient is None:
                # fuck we'll just add it i guess
                return add_db() #will this work?
            patient.rr_id = p_id

        # now update whatever values are given in request.values
        if (patient.phone_number is None and "phone_number" in request.values) or (
           patient.phone_number != request.values.get("phone_number", patient.phone_number)):
            # send a welcome message
            body = ("Welcome to RecordRight! You can text this number to check "
                "information in your record (such as notes from recent visits) "
                "or update personal information. Send any message to begin."
                "Send 'QUIT' at any time to return to the main menu, or 'HELP' for help.")
            client.messages.create(to=request.values["phone_number"], from_="+19182387039", body=body)


        patient.name         = request.values.get('name',         patient.name) # not sure if this is the best way
        patient.birth_day    = int(request.values.get('birth_day',    patient.birth_day))
        patient.birth_month  = int(request.values.get('birth_month',  patient.birth_month))
        patient.birth_year   = int(request.values.get('birth_year',   patient.birth_year))
        patient.phone_number = request.values.get('phone_number', patient.phone_number)
        patient.address      = request.values.get('address',      patient.address)
        patient.notes        = request.values.get('notes',        patient.notes)

        db.session.commit()
        db.session.flush()
        return Response("Successfully updated db", 200, {})
    except Exception as e:
        print("Error updating db: {}".format(e))
        return Response("Error updating db", 200, {})
        
# strip '+' from number if there, and add '1' for US code if needed
def clean_number(from_number):
    if from_number[0] == '+':
        print("stripping '+'")
        from_number = from_number[1:]
    if len(from_number) == 10:
        print("adding '1'")
        from_number = "1{}".format(from_number)
    print("from_number is now {}".format(from_number))
    return from_number

# Bit of a gnarly function, but its goal is pretty simple
# We take in the body of the SMS, which in general should just be
# a number, and the number that sent the message.
# We then pick the next message to sending, fetching data from the
# records db as appropriate. The message fomatting into xml is done later,
# so the message returned should just be a string. We also return the 
# new menu state to be stored in the user's cookie. These are returned
# as a tuple (resonse_message, new_menu_state)
def process_message(message, from_number, menu_state):
    return_body = ""
    new_menu_state = 0
    print("from_number is {}".format(from_number))
    
    from_number = clean_number(from_number)

    # They can send "HELP" at anytime for help
    # or "QUIT" to return to the main menu
    if message == "HELP":
        (return_body, new_menu_state) = process_help(menu_state)
        return (return_body, new_menu_state) 
    elif message == "QUIT":
        #(return_body, new_menu_state) = process_quit(menu_state)
        return process_message("hello", from_number, 0)

    #TODO some sort of check for more than one patients with the same number
    patients = models_test.Patient.query.filter(models_test.Patient.phone_number == from_number).all()
    if len(patients) == 0:
        # register the phone number to an existing patient record
        if menu_state == 0:
            (return_body, new_menu_state) = process_menu_9(message, from_number)
        elif menu_state == 10:
            (return_body, new_menu_state) = process_menu_10(message, from_number)
        elif menu_state == 11:
            (return_body, new_menu_state) = process_menu_11(message, from_number)

        return (return_body, new_menu_state)
    #if len(patients) > 1:
        #return ("Duplicate numbers...", 0)

    patient = patients[0]
    print("Processing message for {}, have menu_state {}".format(patient.name, menu_state))

    if menu_state == 0:
        (return_body, new_menu_state) = process_menu_0(message, patient)
    elif menu_state == 1:
        (return_body, new_menu_state) = process_menu_1(message, patient)
    elif menu_state == 2:
        (return_body, new_menu_state) = process_menu_2(message, patient)
    elif menu_state == 3:
        (return_body, new_menu_state) = process_menu_3(message, patient)
    elif menu_state == 4:
        (return_body, new_menu_state) = process_menu_4(message, patient)
    else:
        # This is a bug and really shouldn't happen, the above options
        # should be exhaustive. 
        return_body = ("We're sorry, but there has been a grave internal error.")
        new_menu_state = 0

    return (return_body, new_menu_state)

# for a message such as 'notes', 'Notes', 'my notes', 
# attempts to return the correct column value
def select_column(m, patient):
    message = m.lower()
    print("checking column of {}".format(message))
    # a bit hacky... but good enough
    if "name" in message:
        return (patient.name, "name")
    elif "phone" in message or "number" in message:
        return (patient.phone_number, "phone_number")
    elif "address" in message:
        return (patient.address, "address")
    elif "notes" in message:
        return (patient.notes, "notes")
    elif "dob" in message or "birth" in message:
        # this is a bit of an odd one because we split
        # the dob accross 3 columns
        return ("{}/{}/{}".format(patient.birth_year, patient.birth_month, patient.birth_day), "dob")
    else:
        print("address in message? {}".format("address" in message))
        return (None, None)

## All process_menu_x functions should take in the message and the patient record
## as arguments, and return a tuple of (return_body, new_menu_state)

def process_menu_0(message, patient):
    # This is the first message, the content of it 
    # isn't at this time important, we just give them
    # the options
    return (("Welcome to RecordRight, text '1' to fetch information, "
             "'2' to update information in your record, or '3' for more help. "
             "At any time, you can send 'HELP' to get more information.")
            , 1)

def process_menu_1(message, patient):
    # They should have selected either fetch (1), update (2), or help (3)
    try:
        req = int(message)
        if req == 1:
            return_body = ("Please reply with the name of the field you want fetched. Fields are: "
                           "date of birth, name, address, or notes.")
            new_menu_state = 2
        elif req == 2:
            return_body = ("Please reply with the name of the field you want updated.  Fields are: "
                           "date of birth, name, address, or notes.")
            new_menu_state = 3
        elif req == 3:
            return_body = ("You can ask for information from your medical record"
                           " by replying with '1', you will be then asked what information"
                           " you want to retrieve (address, notes, etc.). Or you can update"
                           " something in your record, such as your address, by replying with '2'.")
            new_menu_state = 1
        else:
            return_body = "Not a valid option, text 1 to fetch, 2 to update, or 3 for help."
            new_menu_state = 1
    except:
        return_body = ("We're sorry, but there has been an internal error.")
        new_menu_state = 0
    return (return_body, new_menu_state)

def process_menu_2(message, patient):
    # body should contain name of the field they want
    return_body = "Error"
    new_menu_state = 0
    (return_body, colname) = select_column(message, patient)
    if colname is None:
        # error selecting that column
        return_body = "Unknown field {}. Please select from: name, date of birth, phone number, address, or notes.".format(message)
        new_menu_state = 2
    else:
        return_body = ("{} is currently \"{}\". Text '1' to view a different field, "
                       "'2' to update information in your record, or '3' for more help.").format(message, return_body)
        new_menu_state = 1 # for now
    return (return_body, new_menu_state)

def process_menu_3(message, patient):
    # body should contain name of the field they want
    return_body = "Error"
    new_menu_state = 0
    (cur_data, colname) = select_column(message, patient)
    if colname is None:
        return_body = "Unknown field {}. Please select from: name, date of birth, phone number, address, or notes.".format(message)
        new_menu_state = 3
    else:
        extra = " in YYYY/MM/DD format" if colname == "dob" else ""
        return_body = "Current value for this field is \"{}\". Please reply with a new value{}.".format(cur_data, extra)
        new_menu_state = 4
        session['field'] = colname
    return (return_body, new_menu_state)

def process_menu_4(message, patient):
    return_body = "Error"
    new_menu_state = 0
    # body should contain new value, session['field'] should hold the field to update
    try:
        col = session['field']
        if col == "dob":
            try:
                dob = datetime.datetime.strptime(message, "%Y/%m/%d")
            except:
                return_body = ("Error parsing date: please try again with "
                               "a correctly formatted date (ex: 1999/03/01)")
                new_menu_state = 4
            else:
                patients = db.session.query(models_test.Patient).\
                           filter(models_test.Patient.id == patient.id).\
                           update({"birth_year":dob.year, "birth_month":dob.month, "birth_day":dob.day})
                db.session.commit()
                return_body = ("Success, thank you for using RecordRight. Text '1' to fetch information, "
                               "'2' to update information in your record, or '3' for more help.")

                new_menu_state = 1
        else:
            # NB: all fields except dob are strings, so we automatically wrap the
            # value in quotes, as dob is handled previously. 
            print("Updating, setting {} to {} where id = {}".format(col,message,patient.id))
            stmt = text("UPDATE patients SET {} = '{}' WHERE id = {}".format(col, message, patient.id))
            db.engine.execute(stmt)
            return_body = ("Success, thank you for using RecordRight. Text '1' to fetch information, "
                               "'2' to update information in your record, or '3' for more help.")
            new_menu_state = 1
        # save update info
        save_info(col, message, patient.rr_id)
    except Exception as e:
        print("Error: {}".format(e))
        return_body = "Error updating {} to {}".format(session.get('field', 'unkown field'), message)
        new_menu_state = 0
    return (return_body, new_menu_state)

def save_info(col, message, rr_id):
    #client_id = int(request.values['client_id']) # wait this doesn't make any sense
    client_ids = db.session.query(models_test.Updates, models_test.Updates.client_id).all()
    client_ids = [obj[1] for obj in client_ids]
    for client_id in client_ids:
        updates = db.session.query(models_test.Updates).\
                  filter(models_test.Updates.client_id == client_id).first()

        timestamp = time.time()
        new_update = (rr_id, col, message, timestamp)
        if updates is None:
            updates = models_test.Updates(data=[new_update], client_id=client_id)
            db.session.add(updates)
        elif updates.data is None:
            updates.data = [new_update]
        else:
            updates.data.append(new_update)
    db.session.commit()

# The phone number doesn't exist in the db, so lets add it!
def process_menu_9(message, number): 
    return (("Welcome to RecordRight, your phone number doesn't exist in "
             "our database. If you would like to add it to your record, please "
             " respond with your full name."), 
            10)

# message should contain the patients name, nothing else
def process_menu_10(message, number):
    patients = models_test.Patient.query.filter(models_test.Patient.name == message).all()
    return_body = ""
    new_menu_state = 0
    if len(patients) == 0:
        # ruh roh
        return_body = ("Sorry, but we couldn't find your name in our "
                       "database, please contact your hospital/clinic.")
        new_menu_state = 0
    else:
        session['patient_name'] = message
        return_body = ("Please confirm by replying with your date of birth "
                       "in YYYY-MM-DD format.")
        new_menu_state = 11
    return (return_body, new_menu_state)

# message should contain DOB YYYY-MM-DD
def process_menu_11(message, number):
    name = ""
    try:
        name = session['patient_name']
    except:
        return ("Error", 0)
    print("processing dob stuff for {}".format(name))
    if name is None:
        return_body = "There has been an internal error."
        new_menu_state = 0
    else:
        try:
            dob = datetime.datetime.strptime(message, "%Y-%m-%d")
        except:
            return_body = ("Error parsing date: please try again with "
                           "a correctly formatted date (ex: 1999-03-01)")
            new_menu_state = 11
        else:
            patients = models_test.Patient.query.filter(models_test.Patient.name == name).\
                                     filter(models_test.Patient.birth_year == dob.year).\
                                     filter(models_test.Patient.birth_month == dob.month).\
                                     filter(models_test.Patient.birth_day == dob.day).all()
            if len(patients) == 0:
                return_body = ("Your date of birth does not match, please try again"
                               " or contact your hospital/clinic.")
                new_menu_state = 11
            elif len(patients) > 1:
                return_body = ("There are duplicate records, please contact your hospital/clinic"
                               " to resolve this.")
                new_menu_state = 0
            else:
                patient = patients[0]
                print("updating {}'s phone number, currently {}".format(patient.name, patient.phone_number))
                # I don't know why this isn't working, but it doesn't
                #patient.phone_number = number
                # This works instead, don't know why
                patients = db.session.query(models_test.Patient).\
                           filter(models_test.Patient.id == patient.id).\
                           update({"phone_number" : number})
                print("number is now {}".format(patient.phone_number))
                db.session.commit()
                db.session.flush()
                return_body = ("Success! We have updated your record with your phone number."
                               " You can now reply with '1' to fetch information, '2' to"
                               " update information, or '3' for help.")
                new_menu_state = 1
    session['patient_name'] = name
    return (return_body, new_menu_state)

def process_help(menu_state):
    return_body = "No help for you sorry"
    new_menu_state = menu_state

    return (return_body, new_menu_state)

@app.route('/get_update', methods=['GET'])
@requires_auth
def get_update():
    try:
        print("received update req")
        client_id = int(request.values['client_id'])
        updates = db.session.query(models_test.Updates).\
                  filter(models_test.Updates.client_id == client_id).first()
        return jsonify(updates.data)
    # get the client id
    # open its file
    # send back data
    except Exception as e:
        print("Error fetching update: {}".format(e))
        return Response("Error fetching update", 200, {})

@app.route('/update_ack', methods=['GET'])
@requires_auth
def update_ack():
    # get client id
    # get timestamp being acked
    # wipe data
    try:
        print("received ack")
        client_id = int(request.values['client_id'])
        last_timestamp = float(request.values['timestamp'])
        updates = db.session.query(models_test.Updates).\
                  filter(models_test.Updates.client_id == client_id).first()
        updates.data = [(rrid, col, m, timestamp) for (rrid, col, m, timestamp) in
                        updates.data if timestamp < last_timestamp]
        db.session.commit()
        return Response("Cleaned up, thanks", 200, {})
    except Exception as e:
        print("Error acking update: {}".format(e))
        return Response("Error processing ack", 200, {})


if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
    
