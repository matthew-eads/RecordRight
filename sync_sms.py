from app.models import Patient
from app.database import session
from requests_futures.sessions import FuturesSession
from requests.auth import HTTPBasicAuth
import requests
import pickle
import time
import os.path

#run this periodically

#might not need to bother with async stuff if we're a standalone script
RRSMS_URL = "http://record-right.herokuapp.com"
#RRSMS_URL = "http://localhost:5001"

def main():
    # grab the last timestamp file, get the timestamp
    # ask RRSMS_URL for some fresh data
    username='admin'
    pwd='pickabetterpassword'
    client_id='1'
    resp = requests.get("{}/get_update".format(RRSMS_URL), timeout=60, params={"client_id":client_id}, auth=HTTPBasicAuth(username, pwd))
    # unpickle the data 
    data = resp.json()
    timefile_n = ".timestamps/client{}timestamp".format(client_id)
    new_file = not os.path.isfile(timefile_n)
    mode = 'w+' if new_file else 'r+'
    timefile = open(timefile_n, mode)
    max_time = 0
    if new_file:
        last_time = 0
    else:
        last_time = float(timefile.read())
    for update in data:
        (rrid, field, newval, timestamp) =  (update[0], update[1], update[2], update[3])
        if timestamp > max_time:
            max_time = timestamp
        if timestamp < last_time: 
            continue
        patient = session.query(Patient).filter(Patient.id == rrid).first()
        update_patient(patient, field, newval)
        
    session.commit()
    timefile.seek(0)
    timefile.write(str(max_time))
    timefile.truncate()
    timefile.close()
    
    requests.get("{}/update_ack".format(RRSMS_URL), timeout=60, params={"client_id":client_id, "timestamp":str(max_time)},
                 auth=HTTPBasicAuth(username, pwd))
  
def update_patient(patient, field, newval):
    colname = field.lower()
    print(("checking column of {}".format(colname)))
    # a bit hacky... but good enough
    if "name" in colname:
        patient.name = newval
    elif "phone" in colname or "number" in colname:
        patient.phone_number = newval
    elif "address" in colname:
        patient.address = newval
    elif "notes" in colname:
        pass # eh
    elif "dob" in colname or "birth" in colname:
        patient.DOB = newval # TODO make sure this is right format

if __name__ == '__main__':
    main()
