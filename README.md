# RecordRight
### Services for using a Electronic Medical Record System tailored to developing 
regions

See Proposal.md for more background information (our project proposal).


## How to use

* You'll need to install sqlite3 `apt-get install sqlite3` or whatever.
* To run the web interface, install python2.7 and virtualenv. You should
 then be able to run `virtualenv venv -p python2.7` followed by `source venv/bin/activate`
 and finally `pip install -r requirements.txt`.
* Now, you should be able to simply run `python run.py` and navigate to `http://localhost:5000`
* The scheduling components rely on 'cron' and 'at', so you'll need to make sure those are 
installed for scheduling to work. 
* To receive any SMS, you'll need to register your phone number with Twilio,
the best way to do this is to [email Matt](mailto:matteads@gmail.com) your phone
number. I'll add it to Twilio, you'll receive a confirmation code, and then once you
email me the confirmation code, I'll confirm you and you'll be all set.
* Your other option is to run the SMS server locally, and connect with the
fake phone script. To do this, cd into the RRSMS directory. You'll now 
need python 3 (sorry), and run `virtualenv venv -p python3` followed by `source venv/bin/activate`
and then `pip install -r requirements.txt`. To run the server: `python Server.py`, and
run the 'phone' with `python Phone.py -n <a phone number>`. You can then 'text' the server.
The website will still send stuff to the heroku app by default, you can change this by
opening app/views.py, near the top you'll see: `RRSMS_URL = "http://record-right.herokuapp.com"   # RRSMS_URL = "http://localhost:5001"`,
just switch these around and it should then communicate with the local server.

* That should more or less cover it, let me know if you run into any bugs/dependency issues
and I'll do my best to fix them. 
