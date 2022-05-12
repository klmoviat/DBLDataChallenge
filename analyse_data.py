
#Deze code can je in de python console (onderaan)
#copy pasten en runnen
#je krijgt dan rechts de variabelen te zien die overal zitten
#van 1 rij van 1 file
#NOTE: pas wel aan in welke directory je zit!
#gebruik : 'C:\\map\\map\\map\\file.json'
#HET VOORDEEL is dat je makkelijk de structuur van 1 entry
#kan zien, en nested dictionaries makkelijk kan lezen
#gebruik bv de console om doc['entities']['user_mentions']
#te extracten, of andere soortgelijke dingen
#dan kan je ze later toevoegen aan de efficient loading ding

#alle info die je kan extracten staat in doc: als je die expand
#staan alle kolommen van de json erin, en kan je de nested dictionaries
#ook expanden
import pandas as pd
import json
data=[]

cols = ['id_str', 'truncated']
with open('D:\\data\\airlines-1558527599826.json', encoding='latin-1') as f:
    for line in f:
        doc = json.loads(line)
        lst = [doc['id_str'], doc['truncated']]
        data.append(lst)
dftemp = pd.DataFrame(data=data, columns=cols)