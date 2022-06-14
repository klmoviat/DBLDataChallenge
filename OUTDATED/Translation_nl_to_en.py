import json
import glob
import numpy as np
import pandas as pd
import csv, sqlite3

pd.set_option('display.max_colwidth', 500)

!pip install textblob
from textblob import TextBlob as tb

def dutch_trans(tweet):
    try:
        tweet = tb(tweet).translate(from_lang='nl', to='en')
        return str(tweet)
    except:
        tweet = 'und'
        
#conn4 --> SeptData_lang.sqlite database in use (19924 records)
offset1 = 0

for i in range(1,11):
    print(i, offset1)
    query_all = """
    SELECT text
    FROM main
    where lang == 'nl'
    limit 2000 offset """+ str(offset1) +""";
    """
    
    df1=pd.read_sql_query(query_all, conn4)
    df1[['translate']] = df1['text'].apply(dutch_trans)

    if i == 1:
        df2=df1.copy()
        df3=df1.copy()
        print(df2.count())
    else:
        print('....appending df1 to df2...')
        df2 = df2.append(df1)
        df3 = pd.concat([df3, df1])
        print(df2.count())

    offset1 +=2000

df2.to_sql('trans_nl_to_en', conn4, if_exists='replace', index=False)