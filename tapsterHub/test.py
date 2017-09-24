import pandas as pd
import sqlite3
import requests

# conn = sqlite3.connect("bar.db")
# df = pd.read_csv("drinks.csv")

# for index, row in df.iterrows():
#     print(row[0])


r = requests.post("http://localhost:8080/addTab",data={'drink_name':"Happy Gilmore"})
print(r.json())