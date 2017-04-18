#!flask/bin/python
from app import app
# is there a particular reason this was altered?
# app.run(debug=True, host='192.168.124.137')
app.run(debug=True)
