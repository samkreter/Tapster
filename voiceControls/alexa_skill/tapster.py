import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def punch_in():

    welcome_msg = 'What would you like to drink?'

    return question(welcome_msg)


@ask.intent("MakeDrinkRequest")

def answer(drink):
	
    return statement("Making a " + drink)


if __name__ == '__main__':

    app.run(debug=True)