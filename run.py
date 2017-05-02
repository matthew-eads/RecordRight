#!flask/bin/python
from app import app
# is there a particular reason this was altered?
#app.run(debug=True, host='192.168.220.129')

app.run(debug=True, host=app.config['URL'])