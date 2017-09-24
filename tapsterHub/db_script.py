import sqlite3


conn = sqlite3.connect("bare.db")

conn.execute('''
    CREATE TABLE IF NOT EXISTS Ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    );
''')

conn.execute('INSERT INTO Ingredient(name) VALUES ("Rum");')


conn.execute('INSERT INTO Ingredient(name) VALUES ("Coke");')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Drink (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    );
''')


conn.execute('INSERT INTO Drink(name) VALUES ("Rum and Coke");')

conn.execute('''
    CREATE TABLE IF NOT EXISTS Ingredients_Drinks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_id INTEGER REFERENCES Ingredient(id),
        drink_id INTEGER REFERENCES Drink(id),
        ratio TEXT NOT NULL
    );
''')

conn.execute('INSERT INTO Ingredients_Drinks(ingredient_id,drink_id,ratio) VALUES(1,1,"1");')
conn.execute('INSERT INTO Ingredients_Drinks(ingredient_id,drink_id,ratio) VALUES(2,1,"3");')

conn.execute('''
    SELECT Drink.name, Ingredient.name, Ingredients_Drinks.ratio
    FROM Drink
    JOIN Ingredients_Drinks ON (Drink.id = Ingredients_Drinks.drink_id)
    JOIN Ingredient ON (Ingredients_Drinks.ingredient_id = Ingredient.id)
    WHERE Drink.name = "Rum and Coke";
''')
