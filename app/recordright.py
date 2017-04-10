# recordright.py

# recordright.py

from flask import Flask
from flask import render_template
import sys
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

def main():
	hello_world()

if __name__ == '__main__':
	sys.exit(main())

