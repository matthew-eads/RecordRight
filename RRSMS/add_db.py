## Adds a patient record to the database at the specified url
## url defaults to localhost:5000, but can be changed with the -u/--url arg
## (do not add /update to the url - that is done automatically)
## username and password for the db are provided from stdin (if the db
## doesn't need a username/password, just put whatever)
## full name, birth year, birth month, birth day, and phone number are
## then read in from stdin, and sent to the server.

import requests, argparse, sys
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", default="http://localhost:5001")
parser.add_argument("-c", "--credentials", help="Specify a file containing the username and password")
args = parser.parse_args(sys.argv[1:])

url = args.url

if args.credentials is None:
    username = input("username: ")
    pwd = input("password: ")
    print("")
else:
    f = open(args.credentials, "r")
    username = f.readline()[:-1]
    pwd = f.readline()[:-1]
    f.close()

name = input("full name: ")
birth_year = input("birth_year: ")
birth_month = input("birth_month ('1' not 'Jan'): ")
birth_day = input("birth_day: ")
phone_number = input("phone_number: ")
address = input("address: ")
notes = input("notes: ")

data = {"name":name, "birth_year":birth_year, "birth_month":birth_month, 
        "birth_day":birth_day, "phone_number":phone_number, "address":address, "notes":notes}

response = requests.post("{}/add".format(url), params=data, auth=HTTPBasicAuth(username, pwd))
print(response.text) 
