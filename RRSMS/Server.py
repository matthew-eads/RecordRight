import twilio.twiml
import sys
import argparse
from flask import Flask, request, redirect, session, make_response

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--production', action='store_true')

args = parser.parse_args(sys.argv[1:])
production = args.production

SECRET_KEY = 'top secret'
app =  Flask(__name__) 
app.config.from_object(__name__)

@app.route('/', methods=["GET", "POST"])
def main():
    
    #print(str(request.data))
    #print(str(request.values))
    print("from: {0}, body {1}".format(request.values.get('From', None), request.values.get('Body', None)))
    return_body = process_message(request.values.get('Body', None), request.values.get('From', None))
    session['foo'] = 'bar'
    twilio_resp = twilio.twiml.Response()
    twilio_resp.message(return_body)
    resp = make_response(str(twilio_resp))
    resp.set_cookie('menu_state', str(session['menu_state']))
    
    return resp
    
def process_message(message, from_number):
    return_body = ""
    menu_state = session.get('menu_state', 0)
    print("Processing message, have menu_state {}".format(menu_state))
    if message is None or from_number is None:
        # We received a badly formed message, be upset
        return_body = ("We're sorry, but there has been an internal error."
                       "Please try sending your message again")
        
    elif menu_state == 0:
        # This is the first message, the content of it 
        # isn't at this time important, we just give them
        # the options
        return_body = ("Welcome to RecordRight, text '1' to fetch information, "
                       "'2' to update information in your record, or '3' for more help.")
        session['menu_state'] = 1
        return return_body
    elif menu_state == 1:
        # They should have selected either fetch (1), update (2), or help (3)
        try:
            req = int(message)
            if req == 1:
                return_body = ("Fetch feature not yet implemented.")
                session['menu_state'] = 0
            elif req == 2:
                return_body = ("Update feature not yet implemented.")
                session['menu_state'] = 0
            elif req == 3:
                return_body = ("Help feature not yet implemented.")
                session['menu_state'] = 0
            else:
                return_body = "Not a valid option, text 1 to fetch, 2 to update, or 3 for help."
                session['menu_state'] = 0
        except:
            return_body = ("We're sorry, but there has been an internal error."
                           "Please try sending your message again")
    else:
        # This is a bug and really shouldn't happen, the above options
        # should be exhaustive. 
        return_body = ("We're sorry, but there has been a grave internal error.")
        session['menu_state'] = 0

    return return_body
        
if __name__ == '__main__':
    app.run(debug=True)
    
