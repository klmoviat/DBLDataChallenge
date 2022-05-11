import json
import glob
import numpy as np
import pandas as pd
import csv, sqlite3


files = glob.glob("D:\data\*.json") # locatie alle json bestanden lokaal
#de 0 staat er zodat hij alleen maar bestanden die eindigen in 0 meeneemt

df = pd.DataFrame() #maak dataframe

#loop over alle gevonden lokaties, maak van ieder bestand een df en cocat ze
for count,ele in enumerate(files[0:7],len(files[0:7])):
    print(ele)
    dftemp=pd.read_json(ele,lines=True)
    print(dftemp.iloc[0,0])
    df = pd.concat([df, dftemp])

df['display_text_range']=df['display_text_range'].astype(str)
df.iloc[:, 12]=df.iloc[:, 12].astype(str) #note: to_sql kan niet omgaan met \NULL
df.iloc[:, 22]=df.iloc[:, 22].astype(str) #als hij text verwacht, daarom al deze
df.iloc[:, 23]=df.iloc[:, 23].astype(str) #kolommen naar text doen
df.iloc[:, 30]=df.iloc[:, 30].astype(str) #also hij vond arrays niet leuk
df.iloc[:, 31]=df.iloc[:, 31].astype(str) #also hij vond de kolommen met nested
df.iloc[:, 15]=df.iloc[:, 15].astype(str) #info niet leuk
df.iloc[:, 34]=df.iloc[:, 34].astype(str)
df.iloc[:, 35]=df.iloc[:, 35].astype(str)
df.iloc[:, 13]=df.iloc[:, 13].astype(str)
df.iloc[:, 14]=df.iloc[:, 14].astype(str)
df.iloc[:, 36]=df.iloc[:, 36].astype(str)
#df.iloc[:, 37]=df.iloc[:, 37].astype(str)
df.iloc[:, 11]=df.iloc[:, 11].astype(str)
df.iloc[:, 16]=df.iloc[:, 16].astype(str)
df.iloc[:, 0]=df.iloc[:, 0].astype(str)
df.iloc[:, 19]=df.iloc[:, 19].astype(str)
df.iloc[:, 20]=df.iloc[:, 20].astype(str)
df.iloc[:, 26]=df.iloc[:, 26].astype(str)
df.iloc[:, 33]=df.iloc[:, 33].astype(str)



conn = sqlite3.connect("DataChallenge.sqlite")
cursor = conn.cursor()

#maak er een sql ding van

df.to_sql('Full', conn, if_exists='replace', index=False)


