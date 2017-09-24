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
    #Add your shit route stuff here

    return_json = {
        'settings':"null",
        'drink': [{'name':'coke','ratio':3}, {'name':'rum', 'ratio':1}]
    }

    return json.dumps(return_json)


## INSTRUCTIONS

## RUN python3 carter_server.py

## Go to localhost:8000 to see the api

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)