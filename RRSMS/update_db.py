import requests, argparse, sys
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", default="http://localhost:5000")
args = parser.parse_args(sys.argv[1:])

url = args.url

username = input("username: ")
pwd = input("password: ")
print("")
name = input("full name: ")
birth_year = input("birth_year: ")
birth_month = input("birth_month: ")
birth_day = input("birth_day: ")
phone_number = input("phone_number: ")

data = {"name":name, "birth_year":birth_year, "birth_month":birth_month, 
        "birth_day":birth_day, "phone_number":phone_number}

response = requests.post("{}/update".format(url), params=data, auth=HTTPBasicAuth(username, pwd))
print(response.text) 
