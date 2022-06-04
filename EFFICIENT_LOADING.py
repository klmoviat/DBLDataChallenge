import json
import glob
import numpy as np
import pandas as pd
import csv, sqlite3
from datetime import datetime

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
#plus dit staat natuurlijk ook gwn in de text zelf

#follower count extracten:
#doc['user']['followers_count']
#doc['user']['friends_count']

#potentie: maak meerdere data=[] variables aan, per nested ding, en maak
#daar andere tabellen van?
#

#vul hier de lokatie van je files in: hij pakt alle json files in de map!
files = glob.glob("D:\\data\\*.json")
#cols maakt de kolommen aan die je wilt hebben, vul in wat je wilt i guess
cols = ['created_at', 'id_str', 'text', 'user_id',
        'in_reply_to_user_id_str','in_reply_to_status_id_str','lang',
        'user_mentions','hashtags','tweet_url']
user_cols = ['id','screen_name', 'created_at','followers_count'
           , 'friends_count', 'verified']
conversations_cols = ['response_tweet', 'tweet', 'time1']

languages = ["en", "es", "fr", "nl", "und", "de", "ja", "ko", "it", "th", "pt", "in", "tr", "pl", "ru", "ar", "ca"]







#, 'time2', 'response_time'

#in data sla je alles op wat je uiteindelijk in je sqlite database yeet, kan je ook meer van maken
main = []
user = []
conversations = []
#maak lege df aan, zal je ook meerdere moeten hebben als we meerdere databases willen maken
df = pd.DataFrame()
#loop_count print uit hoeveel json bestanden hij heeft gemaakt
loop_count = 0

#We moeten nog uitzoeken hoeveel en welke files 1 maand zijn, kan je hieronder invullen
time = input("Run over full database? y/n ")
if time == 'n':
    files = files[231:279]


#pas 'files' aan naar one_month voor 1 maand tabel
for count, ele in enumerate(files, len(files)):
    print(ele) #voor debugging: print de file waar hij mee bezig is
    with open(ele, encoding='latin-1') as f: #pakt file voor file
        for line in f:  #gaat line voor line de file langs
            try:
                doc = json.loads(line)
            except ValueError as e:
                pass
            if not list(doc)[0] == 'delete': #soms in files staat een line die begint met delete, weet niet wat het doet
                                            #maar volgt niet standaard conventie en fucked alles op
                if doc['lang'] in languages: #arbitrary, maar exclude alles dat we niet kunnen lezen

                    #MERGE EXTENDED TWEET EN TEXT ALS TRUNCATED=1
                    if doc['truncated'] == True:
                        doc['text'] = doc['extended_tweet']['full_text']
                        doc['entities'] = doc['extended_tweet']['entities']

                    #HIER KOLOMMEN SELECTEREN
                    #CODE OM USER_MENTIONS TE EXTRACTEN
                    mentions = ''
                    for x in range(len(doc['entities']['user_mentions'])):
                        temp = doc['entities']['user_mentions'][x]['screen_name']
                        if not x == 0:
                            mentions = mentions + ', ' + temp
                        else:
                            mentions = temp
                    #CODE OM HASHTAGS TE EXTRACTEN
                    hashtags = ''
                    for x in range(len(doc['entities']['hashtags'])):
                        hash = doc['entities']['hashtags'][x]['text']
                        if not x == 0:
                            hashtags = hashtags + ', ' + hash
                        else:
                            hashtags = hash
                    #HIER MEER CODE OM TE EDITEN
                    try:
                        doc[cols[0]] = datetime.strptime(doc[cols[0]], "%a %b %d %H:%M:%S %z %Y")
                    except TypeError:
                        pass




                    tweet_url='twitter.com/'+doc['user']['screen_name']+'/status/'+doc['id_str']
                    #lst is nu een 1-d array die bestaat uit alle entries van 1 rij die we willen houden
                    main_lst = [doc[cols[0]], doc[cols[1]], doc[cols[2]], doc['user']['id_str'], doc[cols[4]],doc[cols[5]],doc[cols[6]], mentions,hashtags,tweet_url]
                    user_lst = [doc['user'][user_cols[0]], doc['user'][user_cols[1]], doc['user'][user_cols[2]], doc['user'][user_cols[3]], doc['user'][user_cols[4]], doc['user'][user_cols[5]]]
                    #if doc['in_reply_to_status_id_str'] is not None:
                        #conversations_lst=[doc['in_reply_to_status_id_str'], doc['id_str'], doc['created_at']]
                    #vul deze rij aan de 2-d array data toe
                    main.append(main_lst)
                    if not user:
                        user.append(user_lst)
                    else:
                        user.append(user_lst)
                    #conversations.append(conversations_lst)
            else:
                main=main #niet per se nodig?
    #df = pd.DataFrame(data=data, columns=cols)     oude junk, is langzamer
    #df = pd.concat([df, dftemp])                   idem
    loop_count = loop_count + 1
    print('loop run')           #bijhouden hoeveel files je al hebt gehad
    print(loop_count)
df = pd.DataFrame(data=main, columns=cols)#hier pas maken we een df
df_user = pd.DataFrame(data=user, columns=user_cols)
#df_conversations=pd.DataFrame(data=conversations, columns=conversations_cols)
conn = sqlite3.connect("DataChallenge.sqlite")  #default sqlite3 shit
cursor = conn.cursor()

#maak er een sql ding van

df.to_sql('main', conn, if_exists='replace', index=False)       #creeer table in je datachallenge.sqlite bestand
df_user.to_sql('user', conn, if_exists='replace', index=False)
#df_conversations.to_sql('conversations', conn, if_exists='replace', index=False)
