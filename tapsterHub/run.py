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
    return statment + 'WHERE Drink.id = ' + str(drink_id) +';';




app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World Broski"

#Recieve instructions to have drinks
@app.route('/tab', methods=['POST'])
def tab():

    drink_name = request.form['drink_name']
    settings = request.form['settings']

    if(drink_name != "null"):
        conn = sqlite3.connect("bar.db")
        tab = FifoDiskQueue("tab_file")
        setting_queue = FifoDiskQueue("settings_file")

        drink_id = conn.execute('SELECT id FROM Drink WHERE name LIKE "' + drink_name + '" LIMIT 1;').fetchone()[0]
        print(drink_id)
        tab.push(str(drink_id).encode(encoding='UTF-8'))
        tab.close()

    if (settings != "null"):
        setting_queue.push(settings.encode(encoding='UTF-8'))
        setting_queue.close()

    conn.close()

    return "Good Request Bro"



#Route to send the drink to be made
@app.route('/getTab')
def getTab():
    tab = FifoDiskQueue("tab_file")

    content = []

    t = tab.pop()

    print(t)

    while(t != None):
        t = t.decode(encoding='UTF-8')
        content.append(t)
        t = tab.pop()


    tab.close()
    return json.dumps(content)

#Route to send the drink to be made
@app.route('/tap')
def tap():

    tab = FifoDiskQueue("tab_file")
    current_drink_id = tab.pop()

    if(current_drink_id != None):
        conn = sqlite3.connect("bar.db")
        drink_id = int(current_drink_id.decode(encoding='UTF-8'))

        tab.close()
        cursor = conn.execute(getSerachString(drink_id))

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


