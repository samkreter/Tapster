#!flask/bin/python
from flask import render_template
from flask import Flask
from flask import request

import json
import sqlite3
import requests
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World Broski"

#Recieve instructions to have drinks
@app.route('/tab')
def tab():


#Route to send the drink to be made
@app.route('/tap')
def tap():



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)


