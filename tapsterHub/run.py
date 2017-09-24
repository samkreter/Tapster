#!flask/bin/python
from flask import render_template
from flask import Flask
from flask import request

import json
import sqlite3
import requests
from datetime import datetime
import os
from queuelib import FifoDiskQueue


def getSerachString(drink_id):

    statment  = '''
        SELECT Drink.name, Ingredient.name, Ingredients_Drinks.ratio
        FROM Drink
        JOIN Ingredients_Drinks ON (Drink.id = Ingredients_Drinks.drink_id)
        JOIN Ingredient ON (Ingredients_Drinks.ingredient_id = Ingredient.id)
    '''
    return statment + 'WHERE Drink.id = ' + drink_id +';';




app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World Broski"

#Recieve instructions to have drinks
@app.route('/tab', methods=['GET', 'POST'])
def tab():

    #drink_name = request.form['drink_name']
    drink_name = "Rum and Coke"

    conn = sqlite3.connect("bar.db")
    tab = FifoDiskQueue("tabfile")

    drink_id = conn.execute('SELECT id FROM Drink WHERE name LIKE "' + drink_name + '" LIMIT 1;').fetchone()

    tab.push(drink_id)

    conn.close()




#Route to send the drink to be made
@app.route('/tap')
def tap():

    tab = FifoDiskQueue("tabfile")
    current_drink = tab.pop()

    if(current_drink):
        conn = sqlite3.connect("bar.db")
        cursor = conn.execute(getSerachString(drink_name))

        ingredients = []

        for row in cursor:
            ingredients.append({
                "name": row[1],
                "ratio": row[2]
            })

        drink = {
            "drink_name": row[0],
            "ingredients": ingredients
        }

        response = {"settings":"null","drink":drink}

        return json.dumps(response)

    return json.dumps({"settings": "null", "drink":"null"})


if __name__ == '__main__':
    app.run(debug=True ,host='0.0.0.0',port=8000)


