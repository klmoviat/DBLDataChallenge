# This is a sample Python script
# Press the green button in the gutter to run the script.
from typing import Any

import pandas as pd
import sqlite3
from SQLITE_Queries import *
from datetime import datetime
#df=pd.read_json(r'C:\Users\20161854\Documents\GitHub\DBLDataChallenge\airlines-1558527599826.json',lines=True)
#df.to_csv(r'C:\Users\20161854\Documents\GitHub\DBLDataChallenge\airlines6.csv')

exec(open('EFFICIENT_LOADING.py').read())

conn=sqlite3.connect('DataChallenge.sqlite')
cursor=conn.cursor()


#maak queries in SQLITE_Queries.py met variable, zodat dit niet vol raakt
cursor.execute(QUERY_DUPLICATES)
cursor.execute(QUERY_DUP_USER)
#replies=cursor.execute(QUERY_REPLY)

cursor.executescript(QUERY_REPLY_TABLES)
cursor.executescript(QUERY_HEAD_TAIL)
cursor.executescript(QUERY_HEAD_TAIL_TEXT)

#cursor.execute("DELETE FROM Full where lang NOT LIKE '%en%' AND lang NOT LIKE '%nl%'")

conn.commit()
