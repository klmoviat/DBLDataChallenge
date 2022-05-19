
#extract alle hashtags in een string, kan nuttig zijn?
hashtags=''
for x in range(len(doc['extended_tweet']['entities']['hashtags'])):
    hash=doc['entities']['hashtags'][x]['text']
    if not x==0:
        hashtags=hashtags+ ', '+ hash
    else:
        hashtags=hash
print(hashtags)

#extract user mentions uit extended tweet
mentions=[]
for x in range(len(doc['extended_tweet']['entities']['user_mentions'])):
    ment=doc['extended_tweet']['entities']['user_mentions'][x]['screen_name']
    mentions.append(ment)
print(mentions)

#PROBLEEM: HOE MERGEN WE DE EXTENDED TWEETS IN TEXT OP BASIS VAN TRUNCATED??
if doc['truncated'] == True:
    doc['text']=doc['extended_tweet']['full_text']
    doc['entities']=doc['extended_tweet']['entities']
    #dit werkt wel oke

#KUNNEN OOK EEN FUNCTIE TRUNCATE AANMAKEN IN EEN APART BESTAND DAT DAT DOET, IS MSS NETTER
#PROBLEEM: HOE KUNNEN WE UIT DEZE DATA CONVERSATIES HALEN?
#niet in theorie, maar praktisch gezien


if doc['in_reply_to_user_id_str'] != NULL:
