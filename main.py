# This is a sample Python script
# Press the green button in the gutter to run the script.
from typing import Any

import pandas as pd
import sqlite3
#df=pd.read_json(r'C:\Users\20161854\Documents\GitHub\DBLDataChallenge\airlines-1558527599826.json',lines=True)
#df.to_csv(r'C:\Users\20161854\Documents\GitHub\DBLDataChallenge\airlines6.csv')

conn=sqlite3.connect('DataChallenge.sqlite')
cursor=conn.cursor()


cursor.execute("DELETE FROM Full WHERE extended_tweet NOT LIKE '%KLM%' AND text NOT LIKE '%klm%' AND in_reply_to_screen_name NOT LIKE '%klm%' AND id NOT LIKE '%56377143%'")
cursor.execute("DELETE FROM Full where lang NOT LIKE '%en%' AND lang NOT LIKE '%nl%'")
#cursor.execute("DELETE FROM airlines6 where reply_count NOT LIKE '0'")
conn.commit()
