# This is a sample Python script
# Press the green button in the gutter to run the script.
from typing import Any

import pandas as pd
import sqlite3
#df=pd.read_json(r'C:\Users\20161854\Documents\GitHub\DBLDataChallenge\airlines-1558527599826.json',lines=True)
#df.to_csv(r'C:\Users\20161854\Documents\GitHub\DBLDataChallenge\airlines6.csv')

conn=sqlite3.connect('DataChallenge.sqlite')
cursor=conn.cursor()


cursor.execute("DELETE FROM airlines6 WHERE C5 not like '%klm%'")
cursor.execute("DELETE FROM airlines6 where C30 NOT LIKE '%en%' OR '%nl%'")

conn.commit()
