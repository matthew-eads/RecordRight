import twilio.twiml
import sys,os 
import argparse
import datetime
from flask import Flask, request, redirect, session, make_response
from database_test import db_session, engine
from models_test import Patient
from sqlalchemy.sql import text

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--production', action='store_true')

args = parser.parse_args(sys.argv[1:])
production = args.production

port = int(os.getenv('PORT', '5000'))


SECRET_KEY = 'top secret'
app =  Flask(__name__) 
app.config.from_object(__name__)

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

    #TODO some sort of check for more than one patients with the same number
    patients = Patient.query.filter(Patient.phone_number == from_number).all()
    if len(patients) == 0:
        # hmmm, maybe have feature to register phone number to a name
        if menu_state == 0:
            (return_body, new_menu_state) = process_menu_9(message, from_number)
        elif menu_state == 10:
            (return_body, new_menu_state) = process_menu_10(message, from_number)
        elif menu_state == 11:
            (return_body, new_menu_state) = process_menu_11(message, from_number)

        return (return_body, new_menu_state)
    if len(patients) > 1:
        return ("Duplicate numbers...", 0)
    patient = patients[0]
    print("Processing message for {}, have menu_state {}".format(patient.name, menu_state))
    if message is None or from_number is None:
        # We received a badly formed message, be upset
        return_body = ("We're sorry, but there has been an internal error. "
                       "Please try sending your message again")
        
    elif menu_state == 0:
        (return_body, new_menu_state) = process_menu_0(message, patient)
    elif menu_state == 1:
        (return_body, new_menu_state) = process_menu_1(message, patient)
    elif menu_state == 2:
        (return_body, new_menu_state) = process_menu_2(message, patient)
    elif menu_state == 3:
        (return_body, new_menu_state) = process_menu_3(message, patient)
    
    else:
        # This is a bug and really shouldn't happen, the above options
        # should be exhaustive. 
        return_body = ("We're sorry, but there has been a grave internal error.")
        new_menu_state = 0

    return (return_body, new_menu_state)
        

## All process_menu_x functions should take in the message and the patient record
## as arguments, and return a tuple of (return_body, new_menu_state)

def process_menu_0(message, patient):
    # This is the first message, the content of it 
    # isn't at this time important, we just give them
    # the options
    return (("Welcome to RecordRight, text '1' to fetch information, "
                   "'2' to update information in your record, or '3' for more help.")
            , 1)

def process_menu_1(message, patient):
    # They should have selected either fetch (1), update (2), or help (3)
    try:
        req = int(message)
        if req == 1:
            return_body = ("Please reply with the name of the field you want fetched (ex: 'notes' or 'name').")
            new_menu_state = 2
        elif req == 2:
            return_body = ("Please reply with the name of the field you want updated (ex: 'address').")
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
        return_body = ("We're sorry, but there has been an internal error."
                       "Please try sending your message again")
        new_menu_state = 1 
    return (return_body, new_menu_state)

def process_menu_2(message, patient):
    # body should contain name of the field they want
    message = message.lower()
    return_body = "Error"
    new_menu_state = 0
    try:
        # this is a hack
        stmt = text("SELECT {} FROM patients WHERE name = '{}'".format(message, patient.name))
        conn = engine.connect()
        res = conn.execute(stmt)
        all_results = []
        for row in res:
            all_results.append(row[0])
        return_body = str(all_results[0])
        new_menu_state = 0
    except Exception as e:
        print("Error selecting: {}".format(e))

    return (return_body, new_menu_state)

def process_menu_3(message, patient):
    # body should contain name of the field they want
    message = message.lower()
    return_body = "Error"
    new_menu_state = 0

    return (return_body, new_menu_state)

# The phone number doesn't exist in the db, so lets add it!
def process_menu_9(message, number): 
    return (("Welcome to RecordRight, your phone number doesn't exist in "
             "our database. If you would like to add it to your record, please "
             " respond with your full name."), 
            10)

# message should contain the patients name, nothing else
def process_menu_10(message, number):
    patients = Patient.query.filter(Patient.name == message).all()
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
            patients = Patient.query.filter(Patient.name == name).\
                                     filter(Patient.birth_year == dob.year).\
                                     filter(Patient.birth_month == dob.month).\
                                     filter(Patient.birth_day == dob.day).all()
            if len(patients) == 0:
                return_body = ("Your date of birth does not match, please try again"
                               " or contact your hospital/clinic.")
                new_menu_state = 11
            elif len(patients) > 1:
                return_body = ("There are duplicate records, please contact your hospital/clinic"
                               " to resolve this.")
                new_menu_state = 0
            else:
                patients[0].phone_number = number
                db_session.commit()
                return_body = ("Success! We have updated your record with your phone number."
                               " You can now reply with '1' to fetch information, '2' to"
                               " update information, or '3' for help.")
                new_menu_state = 1
    session['patient_name'] = name
    return (return_body, new_menu_state)

if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
    
