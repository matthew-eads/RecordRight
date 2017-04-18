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
args = parser.parse_args(sys.argv[1:])

url = args.url

username = input("username: ")
pwd = input("password: ")
print("")
pid = input("patient id: ")
data = {"patient_id":pid}
print("enter the fields you want to update and their new values, ex: \"birth_year:1\"")

for line in sys.stdin:
    try:
        split = line.split(':')
        (key,value) = (split[0].strip(), split[1].strip())
        data[key] = value
    except Exception as e:
        print("you fucked up, we weren't able to process this line")


response = requests.post("{}/update".format(url), params=data, auth=HTTPBasicAuth(username, pwd))
print(response.text) 
