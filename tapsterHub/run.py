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



@app.route('/addSettings', methods=['POST'])
def addSettings():

    settings = request.form['settings']

    if (settings != "null"):
        setting_queue = FifoDiskQueue("settings_file")
        setting_queue.push(settings.encode(encoding='UTF-8'))
        setting_queue.close()

        return "sucess"

    return "No settings to update"


@app.route('/createDrink', methods=['POST'])
def createDrink():
    drink_name = request.form['drink']
    return "Hello World Broski"

#Recieve instructions to have drinks
@app.route('/addTab', methods=['POST'])
def addTab():

    drink_name = request.form['drink_name']

    if(drink_name != "null"):
        conn = sqlite3.connect("bar.db")
        tab = FifoDiskQueue("tab_file")

        drink_id = conn.execute('SELECT id FROM Drink WHERE name LIKE "' + drink_name + '" LIMIT 1;').fetchone()

        if(drink_id == None):
            return json.dumps({'success':False,'error':"NoDrinkInDB"}), 400, {'ContentType':'application/json'}

        tab.push(str(drink_id[0]).encode(encoding='UTF-8'))
        tab.close()

        conn.close()

        return json.dumps({'success':True, 'hello':'hey'}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False,'error':"DrinkNameNull"}), 400, {'ContentType':'application/json'}



#Route to send the drink to be made
@app.route('/getTab')
def getTab():
    tab = FifoDiskQueue("tab_file")

    content = []

    t = tab.pop()

    while(t != None):
        t = t.decode(encoding='UTF-8')
        content.append(t)
        t = tab.pop()

    tab.close()
    return json.dumps(content)

@app.route('/registerCabinet', methods=['GET'])
def registerCabinet():

    cabinet_id = request.args.get("cabinet_id")
    if(cabinet_id is None):
        #create id and store in the database
        cabinet_id = 7

    return json.dumbs({'cabinet_id':cabinet_id})

#Route to send the drink to be made
@app.route('/tap',methods=['GET'])
def tap():

    cabinet_id = request.args.get("cabinet_id")
    if(cabinet_id is not None):

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

    else:
        return json.dumps({'success': False,'error':"Must Have Cabinet ID to access to tap"}), 400, {'ContentType':'application/json'}


if __name__ == '__main__':
    app.run(debug=True ,host='0.0.0.0',port=8080)


