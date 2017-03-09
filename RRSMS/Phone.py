import http.client, urllib
import argparse, sys
import random
import xml.etree.ElementTree as ET

# Simulates a phone which texts our twilio flask app
# pass in configuration details on command line  (url, port, phone #, etc)
# and then interact on the command line; type in text to send an sms message,
# and the response is then shown. 

def random_phone_number():
    number = ""
    for x in range(0,10):
        number += str(random.randint(0,9))
    return number

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", default="localhost")
    parser.add_argument("-p", "--port", default="5000")
    parser.add_argument("-n", "--number", help="This is the pretend phone number to use",
                        default=random_phone_number())
    args = parser.parse_args(sys.argv[1:])
    url = args.url
    port = args.port
    number = args.number
    print("u: {0}, p: {1}, n: {2}".format(url,port,number))
    conn = http.client.HTTPConnection("{0}:{1}".format(url, port))

    header = {"Content-type" : "application/x-www-form-urlencoded", "Accept":"text/plain"}
    
    print("Welcome, please enter the message you want to send")
    while True:
        message = ""
        try:
            message = input()
        except EOFError:
            print("Goodbye.")
            break

        if message.lower() in ["quit", "exit", "q"]:
            print("Goodbye.")
            break
        
        data = urllib.parse.urlencode({"From":number, "Body":message})
        conn.request("POST", "/", data, header)
        response = conn.getresponse()
        if response.status != 200:
            print("Got bad response: {0}".format(response.status))
        else:
            response_message = response.read()
            root = ET.fromstring(response_message)
            bodies = root.findall(".//Body")
            if len(bodies) != 1:
                print("Too many bodies... here is the raw xml:")
                print(response.read())
            else:
                print(bodies[0].text)
    

if __name__ == "__main__":
    main()
