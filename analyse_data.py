#Deze code can je in de python console (onderaan)
#copy pasten en runnen.
#je krijgt dan rechts de variabelen te zien die overal zitten van 1 rij van 1 file.
#
#NOTE: pas wel aan in welke directory je zit!
#gebruik : 'C:\\map\\map\\map\\file.json'
#HET VOORDEEL is dat je makkelijk de structuur van 1 entry
#kan zien, en nested dictionaries makkelijk kan lezen
#gebruik bv de console om doc['entities']['user_mentions']
#te extracten, of andere soortgelijke dingen
#Als je dan kan extracten wat je wilt, kan je de code toevoegen aan de efficient loading ding

#alle info die je kan extracten staat in doc: als je die expand
#staan alle kolommen van de json erin, en kan je de nested dictionaries
#ook expanden
import pandas as pd
import json
data=[]
stop_line=14343    #als je een specifieke line hebt die je interessant lijkt om te zien (bv een hele lange, veel nested shit)
count=0         #count hoeveel loops, helpt met hierboven beschreven
cols = ['id_str', 'truncated']
with open('D:\\data\\airlines-1558527599826.json', encoding='latin-1') as f:
    for line in f:
        if count<stop_line:

            doc = json.loads(line)
            if not list(doc)[0] == 'delete':
                lst = [doc['id_str'], doc['truncated']]
                if doc['truncated'] == True:
                    doc['text'] = doc['extended_tweet']['full_text']
                    doc['entities'] = doc['extended_tweet']['entities']
                data.append(lst)
                count=count+1
        else:
            data=data
dftemp = pd.DataFrame(data=data, columns=cols)