import json
import glob
import numpy as np
import pandas as pd
import csv, sqlite3

#AANGEPASTE LOADING: VEEEEEEL SNELLER
#voeg de kolommen toe aan cols hieronder die je wilt houden
#extend de doc[cols[i]] array in de for loop daaronder tot het aantal elements
#in cols
#50 json files in like 1.2 min ofzo

files = glob.glob("D:\data\*0.json")
cols = ['created_at', 'id_str', 'text', 'truncated', 'in_reply_to_screen_name', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count', 'favorited', 'retweeted','lang']
data = []
df = pd.DataFrame()

for count,ele in enumerate(files,len(files)):
    print(ele)
    with open(ele, encoding='latin-1') as f:
        for line in f:
            doc = json.loads(line)
            if not list(doc)[0] == 'delete':
                lst = [doc[cols[0]], doc[cols[1]], doc[cols[2]], doc[cols[3]], doc[cols[4]], doc[cols[5]], doc[cols[6]], doc[cols[7]], doc[cols[8]], doc[cols[9]], doc[cols[10]], doc[cols[11]]]
                data.append(lst)
            else:
                data=data
    dftemp = pd.DataFrame(data=data, columns=cols)
    data = []
    df = pd.concat([df, dftemp])

conn = sqlite3.connect("DataChallenge.sqlite")
cursor = conn.cursor()

#maak er een sql ding van

df.to_sql('Full', conn, if_exists='replace', index=False)
