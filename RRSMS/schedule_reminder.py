from twilio.rest import TwilioRestClient
import argparse
import sys
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--message", help="Specify message to send. If not specified, message is read from stdin")
parser.add_argument("-n", "--number", help="Specify number of recepient. If not specified, number is read from stdin")
parser.add_argument("-t", "--time", help="When to send the message")
parser.add_argument("-d", "--dry-run", action="store_true", help="If specified, doesn't actually send the message")
args = parser.parse_args(sys.argv[1:])

body = args.message if args.message is not None else input("Enter message to send: ")
to_number = args.number if args.number is not None else input("Enter number to send to: ")
date = args.time if args.time is not None else input("Enter date to send reminder: ")


command = "{}/send_reminder.bash -n {} -m \"{}\"".format(os.path.dirname(os.path.abspath(__file__)), to_number, body)
print("command is {}".format(bytes(command, "ascii")))
proc = subprocess.Popen(['at', date], stdin=subprocess.PIPE)
proc.stdin.write(bytes(command, "ascii"))
proc.stdin.close()


