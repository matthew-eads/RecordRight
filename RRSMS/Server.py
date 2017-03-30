import twilio.twiml
import sys,os 
import argparse
from flask import Flask, request, redirect, session, make_response
from database_test import scoped_session
from models_test import Patient

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
    patient = Patient.query.filter(Patient.phone_number == from_number).first()
    print("Processing message for {}, have menu_state {}".format(patient.name, menu_state))
    if message is None or from_number is None:
        # We received a badly formed message, be upset
        return_body = ("We're sorry, but there has been an internal error. "
                       "Please try sending your message again")
        
    elif menu_state == 0:
        # This is the first message, the content of it 
        # isn't at this time important, we just give them
        # the options
        return_body = ("Welcome to RecordRight, text '1' to fetch information, "
                       "'2' to update information in your record, or '3' for more help.")
        new_menu_state = 1
    elif menu_state == 1:
        # They should have selected either fetch (1), update (2), or help (3)
        try:
            req = int(message)
            if req == 1:
                return_body = ("Fetch feature not yet implemented.")
                new_menu_state = 0
            elif req == 2:
                return_body = ("Update feature not yet implemented.")
                new_menu_state = 0
            elif req == 3:
                return_body = ("Help feature not yet implemented.")
                new_menu_state = 0
            else:
                return_body = "Not a valid option, text 1 to fetch, 2 to update, or 3 for help."
                new_menu_state = 0
        except:
            return_body = ("We're sorry, but there has been an internal error."
                           "Please try sending your message again")
    else:
        # This is a bug and really shouldn't happen, the above options
        # should be exhaustive. 
        return_body = ("We're sorry, but there has been a grave internal error.")
        new_menu_state = 0

    return (return_body, new_menu_state)
        
if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
    
