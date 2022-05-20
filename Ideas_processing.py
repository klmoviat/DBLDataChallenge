
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


#CODE VOOR DATE ALS STRING OMZETTEN NAAR DATETIME OBJ ZODAT JE KAN SUBSTRACTEN
from datetime import datetime
date = datetime.strptime(doc['created_at'], "%a %b %d %H:%M:%S %z %Y")

#PROBLEEM: "HEAD" EN TAIL VINDEN VAN CONVERSATION
#VOOR DE TAIL IS EEN QUERY VOLDOENDE IN DE REPLIES TABLE:
SELECT id_str as tail_id
from replies
where id_str NOT IN  (select in_reply_to_status_id_str from replies);


#EXTRACTING CONVERSATIONS
#VOOR DE HEAD HEB IK GEEN CONCREET IDEE MAAR
tail_id.in_reply_to_status_id_str=temp_head
for temp_head in replies.id_str:
    temp_head=temp_head.in_reply_to_status_id_str
head_id=temp_head
#geen idee hoe je dit implement in sql ofzo, maar het idee is
#je pakt de tweet waarop tail_id antwoord, maakt die de tijdelijke head
#zoekt die id op in replies.id_str, en pakt de reply daarop,
#maakt die nieuwe head. laat loopen totdat temp_head niet meer
#in id_str staat, oftewel totdat er geen tweet meer is die er op replied.
#vervolgens wil je head_id en tail_id in een sqlite table zetten.
#MOGELIJKE PROBLEMEN: uiteindelijk willen we natuurlijk sentiment
#analysis doen op de niet KLM tweets. Dus je moet eigenlijk de eerste en laatste
#niet KLM tweet pakken. Daarbovenop moet je een counter toevoegen die bijhoudt
#of je eindresultaat voldoet aan de lengte van een conversation.
#hoe check je of je conversatie tussen klm en 1 klant is, en niet klanten onderling?
#onze data gaat maar over een jaar, het kan zijn dat tweets antwoorden zijn op tweets die we
#niet hebben?/dat er nog tweets antwoorden op onze tweets, maar de antwoorden niet hebben?
#MOGELIJKE OPLOSSINGEN: sla in de for loop twee temp values op, zodat als
#je head klm blijkt te zijn, je de id van daarvoor kan pakken. WEL EEN IDENTIFIER AANPLAKKEN
#ZODAT WE WETEN DAT HET EEN CONVO IS DIE KLM START!!!
#we zouden evt een query kunnen doen die alle tweets droppen die niet van
#KLM zijn of waar KLM niet op gereplied wordt. Je mist dan alleen wel structuur:
#user1<KLM<user2<KLM en uberhaupt user<KLM
