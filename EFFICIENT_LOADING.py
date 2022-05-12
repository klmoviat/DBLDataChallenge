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


#VOORBEELDEN VOOR CODE:
#nested ding extracten:
#doc['entities']['user_mentions']
#Hiermee krijg je bv: {'screen_name': 'British_Airways', 'name': 'British Airways', 'id': 18332190, 'id_str': '18332190', 'indices': [0, 16]}
#weet niet hoe hij met meerdere mentions omgaat?

#follower count extracten:
#doc['user']['followers_count']
#doc['user']['friends_count']

#potentie: maak meerdere data=[] variables aan, per nested ding, en maak
#daar andere tabellen van?
#

#vul hier de lokatie van je files in: hij pakt alle json files in de map!
files = glob.glob("D:\data\*.json")
#cols maakt de kolommen aan die je wilt hebben, vul in wat je wilt i guess
cols = ['created_at', 'id_str', 'text', 'truncated', 'in_reply_to_screen_name', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count', 'favorited', 'retweeted','lang']
#in data sla je alles op wat je uiteindelijk in je sqlite database yeet, kan je ook meer van maken
data = []
#maak lege df aan, zal je ook meerdere moeten hebben als we meerdere databases willen maken
df = pd.DataFrame()
#loop_count print uit hoeveel json bestanden hij heeft gemaakt
loop_count=0

#We moeten nog uitzoeken hoeveel en welke files 1 maand zijn, kan je hieronder invullen
one_month=files[0:30]
#pas 'files' aan naar one_month voor 1 maand tabel
for count,ele in enumerate(files,len(files)):
    print(ele) #voor debugging: print de file waar hij mee bezig is
    with open(ele, encoding='latin-1') as f: #pakt file voor file
        for line in f:  #gaat line voor line de file langs
            doc = json.loads(line)
            if not list(doc)[0] == 'delete': #soms in files staat een line die begint met delete, weet niet wat het doet
                                            #maar volgt niet standaard conventie en fucked alles op
                if doc['lang'] == 'en' or doc['lang'] == 'nl': #arbitrary, maar exclude alles dat we niet kunnen lezen
                    #lst is nu een 1-d array die bestaat uit alle entries van 1 rij die we willen houden
                    lst = [doc[cols[0]], doc[cols[1]], doc[cols[2]], doc[cols[3]], doc[cols[4]], doc[cols[5]], doc[cols[6]], doc[cols[7]], doc[cols[8]], doc[cols[9]], doc[cols[10]], doc[cols[11]]]
                    #vul deze rij aan de 2-d array data toe
                    data.append(lst)
            else:
                data=data #niet per se nodig?
    #df = pd.DataFrame(data=data, columns=cols)     oude junk, is langzamer
    #df = pd.concat([df, dftemp])                   idem
    print('loop run')           #bijhouden hoeveel files je al hebt gehad
    loop_count=loop_count+1
    print(loop_count)
df = pd.DataFrame(data=data, columns=cols)      #hier pas maken we een df
conn = sqlite3.connect("DataChallenge.sqlite")  #default sqlite3 shit
cursor = conn.cursor()

#maak er een sql ding van

df.to_sql('Full', conn, if_exists='replace', index=False)       #creeer table in je datachallenge.sqlite bestand
