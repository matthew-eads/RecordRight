from twilio.rest import TwilioRestClient
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--message", help="Specify message to send. If not specified, message is read from stdin")
parser.add_argument("-n", "--number", help="Specify number of recepient. If not specified, number is read from stdin")
parser.add_argument("-d", "--dry-run", action="store_true", help="If specified, doesn't actually send the message")
args = parser.parse_args(sys.argv[1:])
    
body = args.message if args.message is not None else input("Enter message to send: ")
to_number = args.number if args.number is not None else input("Enter number to send to: ")


ACCOUNT_SID = "ACbaca90abfe93b3a0c75a44d71ed1e0c2"
AUTH_TOKEN = "8b1c193701c6f7332f669d1448ddbc68"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

if not args.dry_run:
    client.messages.create(to=to_number, from_="+19182387039", body=body)
else:
    print("not sending message {} to {}".format(body, to_number))
