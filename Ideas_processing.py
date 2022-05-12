
#extract alle hashtags in een array, kan nuttig zijn?
hashtags=[]
for x in range(len(doc['extended_tweet']['entities']['hashtags'])):
    hash=doc['extended_tweet']['entities']['hashtags'][x]['text']
    hashtags.append(hash)
print(hashtags)

#extract user mentions uit extended tweet
mentions=[]
for x in range(len(doc['extended_tweet']['entities']['user_mentions'])):
    ment=doc['extended_tweet']['entities']['user_mentions'][x]['screen_name']
    mentions.append(ment)
print(mentions)

#PROBLEEM: HOE MERGEN WE DE EXTENDED TWEETS IN TEXT OP BASIS VAN TRUNCATED??

