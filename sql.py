import sqlite3
import pandas as pd
import json

data = [json.loads(line) for line in open('airlines4.json', 'r')]

df = pd.DataFrame(data)
print(df.head())
print(df.columns)

#conn = sqlite3.connect('databasetest.db')
#cursor = conn.cursor()