import twilio.twiml
import sys
import argparse
from flask import Flask, request, redirect

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--production', action='store_true')

args = parser.parse_args(sys.argv[1:])
production = args.production

app =  Flask(__name__) 

@app.route('/', methods=["GET", "POST"])
def main():
    
    #print(str(request.data))
    #print(str(request.values))
    print("from: {0}, body {1}".format(request.values.get('From', None), request.values.get('Body', None)))
    return_body = "message acknowledged"
    
    resp = twilio.twiml.Response()
    resp.message(return_body)
    return str(resp)
    

        
if __name__ == '__main__':
    app.run(debug=True)
    
