import logging

import requests
import json

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

# Routing Info
tapster_hub_host = "http://1a07e97c.ngrok.io"
addTabRoute = '/addTab'
createNewDrink = '/createDrink' 

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def define_new_drink(drink):
    r = requests.post(tapster_hub_host + createNewDrink, data = {'drink_name': drink, Ingredients: [""]})
    return statement("Creating new drink in Database" + drink)

@ask.launch

def punch_in():

    welcome_msg = 'What would you like to drink?'

    return question(welcome_msg)


@ask.intent("MakeDrinkRequest")

def answer(drink):
    r = requests.post(tapster_hub_host + addTabRoute, data = {'drink_name': drink})
    if r.ok:
        return statement("Making a " + drink)
    else:
        error = r.json()['error']
        if error == 'NoDrinkInDB':
            return define_new_drink(drink)
        elif error == "NoIngredients":
            return statement("Missing Ingredients")
        else:
            return statement("Unknown Error Has Occurred")

if __name__ == '__main__':

    app.run(debug=True)