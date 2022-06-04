from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

list_head_sent_algo = []
list_tail_sent_algo = []
def sentiment_analysis(text1, text2):
    # analyse 1st Tweet
    text1 = preprocess(text1)
    encoded_input = tokenizer(text1, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]

    # analyse 2nd Tweet
    text2 = preprocess(text2)
    encoded_input2 = tokenizer(text2, return_tensors='pt')
    output2 = model(**encoded_input2)
    scores2 = output2[0][0].detach().numpy()
    scores2 = softmax(scores2)
    ranking2 = np.argsort(scores2)
    ranking2 = ranking2[::-1]
    for i in range(scores2.shape[0]):
        l = config.id2label[ranking2[i]]
        s = scores2[ranking2[i]]

    # create dictionaries with the sentiment scores of the 1st and 2nd Tweet
    dict = {}
    for i in range(3):
        dict['Negative'] = scores[0]
        dict['Neutral'] = scores[1]
        dict['Positive'] = scores[2]
    dict2 = {}
    for i in range(3):
        dict2['Negative'] = scores2[0]
        dict2['Neutral'] = scores2[1]
        dict2['Positive'] = scores2[2]

    # compare the positive and neg semantic analysis
    max_val = list(dict.values()) ### THIS IS THE SENTIMENT BEFORE ACCORDING TO THE ALGO
    max_ke = list(dict.keys())
    tuple1 = (max_ke[max_val.index(max(max_val))], max(max_val)) # a tuple of the highest sentiment and score
    max_val2 = list(dict2.values())
    max_ke2 = list(dict2.keys())
    tuple2 = (max_ke2[max_val2.index(max(max_val2))], max(max_val2))
    list_head_sent_algo.append(max_ke[max_val.index(max(max_val))])
    list_tail_sent_algo.append(max_ke2[max_val2.index(max(max_val2))])
    return dict, dict2

    # calculate sentiment change (the difference in positive score)
    #delta = (dict['positive'] - dict2['positive'])
    #print(f"difference is {delta} (positive before={dict['positive']}, positive after={dict2['positive']})")


import sqlite3
import pandas as pd

# from sample data

list_head = [
    "@British_Airways Booking auto-complete typing isn't working as normal: when I type FRA for Frankfurt, it offers me 'France' options.  See below. This is wrong - IATA codes should yield actual airport in search / destination field. https://t.co/nmI4a5Y9OT",
    "@British_Airways Can someone help? I have just been passed around your call centre. I have been told to email but there is no where for my specific query. Your advertising flights at a price that you can't get for anywhere close to that cost! Hugely misleading.",
    "@British_Airways Thanks for replying back. I would please like to know whether it's possible to change the departure airport/city of a ticket and if so what the process of doing so?",
    "@British_Airways flying from San Diego to LHR this evening at 2045 I Club. What time does bag drop open? Thanks",
    "@British_Airways thanks for losing my bag. Thanks for being dismal all round. Amazed you are still in business. Theresa May has a better chance of negotiating a successful brexit than you have of not making a clusterfuck of every journey... #shitservice #toflytonotserve",
    "@British_Airways trying to contact you daily by phone and email for 2 weeks. No response and phone cuts me off. Is anyone there to help?",
    "@KLM By chance would you please check flight 590 Accra-Amsterdam 5/22/19. My daughter left journal in seatback 35H. Blue,Dream front, Ghanna entries. Means SO much. 270-993-6598,gwen.roby66@gmail.com",
    "@Klm good morning!Are there currently problems with changing bookings online?I try to adjust the date of my back flight but always run into an error boodscap at the last step?Can you possibly get this in order for me through this road?& GT; & GT;'",
    "@KLM Hi, any chance you can retrieve an old boarding pass for me even though it's been almost 6 months since I boarded that flight? I need a copy of it and I've deleted my email😅",
    "@Klm Oh no!Am I missing this promotion now because I have already proactively booked flights?Just get the mail that you offer a wonderful discount for marathon runners like me.†#Maratonvalencia https://t.co/jbanrwpgyyr'",
    "@KLM Your team mistyped my @Delta Skymiles number at the airport for a recent trip. How do I get the credit for those miles? Is that with you or @Delta ? Thx!:)",
    "@KLM can't book tickets by the app or website, and in queue on phone for ages....what to do?",
    "@Ryanair Can you help with this please?",
    "@Ryanair Can you help? I need to amend my car parking booking at Standsted. I have been on the website but can't find out how to do this?",
    "@Ryanair Hi Ana, is there a cost involved in this?",
    "@Ryanair I would like to cancel my booking due to medical emergency. Request your support please",
    "@Ryanair My son's passport expired in April 2019, a new application is in progress but I am worried it won't arrive before our trip on 7th June, can we use any other form of ID?",
    "@Ryanair can I take a ps4 on to a plane in my hand luggage? Cheers",
    "@Ryanair can you add a 20kg bag online after you have already checked in prior to the flight?",
    "@Ryanair flight was cancelled (21st May, Rome-Catania), earliest option given was next day (22nd May).Had to stay in Rome and now I want to apply for expenses. Form 'EU261' don't accept name, This customer name does not match any name in the reservation. Please check and re-enter",
    "@Ryanair hey team! whats the deal with bluetooth headphones on your flight?",
    "@Ryanair hi have flights booked 20kg bag and seats payed for - are we allowed hand luggage as well - can’t see anything on the booking - thanks",
    "@Ryanair how do I confirm my changes to my flight times you have given me.",
    "@Ryanair please help! Flying from EDI on Fri with a group. One has booked using married name but passport in maiden name. Will we be charged to change this?!",
    "@Ryanair your check-in system seems to be broken. I can't get past the passport page.",
    "@klm last time I fly with you. Yesterday you accepted a booking with a 1 hr Schiphol transfer, then before the flight from Newcastle takes off, suddenly massive delays and all flights missed. And you know you’ve got problems at Schiphol. Dishonesty leading to ruined plans.",
    "@lufthansa Could you please tell me when bag drop opens at Terminal 2 at @HeathrowAirport? I've got a 6:55 am flight in a few weeks and would like to arrange my transport to the airport. Thanks.",
    "@lufthansa I am trying to call your customer service line (USA), and no one is picking up. I thought you had 24hr service?",
    "@lufthansa I tried calling and didn’t pick an option . Again , nothing happened . No answer . I e mailed u guys, no response yet either . What next ?",
    "@lufthansa OK, it is now another week that has passed and nothing. I have yet to even be reimbursed the $98.00 I paid for the selected seats and that is since April 23. At this point I am not at all impressed with @lufthansa customer service department. I need to speak to someone PLEASE.",
    "@lufthansa Tried to check in on my flight to Tampa via Frankfurt later this morning, but after submitting my info, I got a message saying I was not checked in, and needed to get in touch with customer service. Please DM me ASAP.",
    "@lufthansa first time flying, first delay on Amsterdam to Frankfurt because of that we missed our flight to shanghai. Now our trip has a total delay of 5 hours... what do we get; 10 euro vouchers..#Neveragain #disappointed",
    "@lufthansa hi! Is there any problem with the app? I cant't log in, neither see my reservation ☹",
    "@lufthansa i am still waiting for delayed baggage compensation and any update regarding it..you are not replying to my any email. File reference BOMLH74667 Kindly update me status.",
    "@lufthansa i paid to reserve seats for me and my family . Unfortunately I receive email from Lufthansa saying we change your seats. Why??? This is really unexceptable . Im very upset. COM-1434034",
    "@lufthansa is your online checkin unavailable?",
    "@lufthansa lost my case, I'm on a business trip and have lost all training materials, chargers, clothes, toiletries... Nightmare! Terrible experience",
    "@ryanair do i need a passport to fly to wales",
    "@united @lufthansa We’re coming up on the 20 day mark and still no refund. At this point I would just appreciate knowing if you’re just planning on keeping our money so I can stop worrying about it.",
    "Another slow hand clap for @British_Airways and their consistently poor baggage operation at Heathrow. 20 minutes and no sign of anyone’s bags emerging. Well done, people. https://t.co/78MgNdsJAD",
    "Dear @KLM, yesterday on flight KL 0645 from Amsterdam to New York I left my coat in the luggage compartment above row 30 (with my house key in the pocket). Is there a way to get my jacket back? Can this be controlled? Thanks in advance",
    "Big thanks to @airfrance and @KLM  for allowing a delay from BUD to CDG which was scheduled to depart at 12:10 that meant i missed my connecting flight. 6.5 hour wait in CDG and when it comes to boarding, tell me my #flybluepetrolium card doesnt entitle me to priority boarding.",
    "Bye, bye 🇬🇧, hello 🇯🇵 See you in Osaka.  Wish me luck @British_Airways #ba100 #Japan #nervousflyer https://t.co/9mS9zjdOdr",
    "Fantastic service from #KLM leaving my luggage in Amsterdam. Now stand in Strasbourg and can do nothing!",
    "Hello @Ryanair, I’ve just arrived in Oslo from London and realised I’ve left my jacket on the plane 😣 what’s the best way to get it back please?",
    "Hi @British_Airways - when is BEA going back to @HeathrowAirport so that all the retros be reunited again?",
    "Hi @lufthansa on your app, flight 464 is listed as “on time”. It has not left yet. Any update on this?",
    "How come my luggage got into LAX at 12pm after a 24 hour wait and is only being arranged for collection at 5pm by the carrier? I could have turned up to the airport to collect it myself and come back in that time @KLM @KLM_US",
    "Life can get pretty hectic for an international baby on the go. That’s why a premium is placed on rock star travel accommodations. Thanks to the folks at @lufthansa for treating Bishop like he deserves to be treated. #WorldWideBK🌎 #Cheerio https://t.co/PQa4TaxD48",
    "Need tickets for Italy... Gandhi's &amp; Vadra's will confirm in sometime how many they need @IndiGo6E @flyspicejet @airindiain @lufthansa ... @sureshpprabhu - Please recommend &amp; get it done sir..",
    "Nice...today I travel with one of the (four?) new @klm planes! Nice one KLM! https://t.co/gH7CkHq8u9",
    "So @British_Airways left bags for at least a dozen people behind for our flight from London to Florence. Now they are trying to tell us that they can't get our bags to us until Friday.",
    "Still waiting new silver exec card since mid April ☹ @British_Airways",
    "Thank you @KLM ! My flight to Sydney was cancelled and automatically rebooked with a 14 hr delay. But one phone call with your amazing help center later I'm now booked on a different route (a bit more flight time, but hey) and arriving even sooner. YOU ROCK❣❣❣thank you again!",
    "Thanks @British_Airways I really needed the extra 2 hour delay on the flight today with everyone sat on board...",
    "The ongoing lack of flights provided by @British_Airways on Aberdeen to London is really frustrating. I understand that it allows them to charge sky high prices (£364 for a single tomorrow afternoon) but it is poor service",
    "Why are the @British_Airways planes going to Accra filthy and old? This is a waste of money. https://t.co/PPBIzkbCUO",
    "Wow.What a service.I know again why I prefer @klm to fly than certain other companies.Did I find out this morning that I had booked my flight for Friday instead of Saturday and turned it into Saturday without any problems.Plume for #klm!",
    "luggage missing - cust services unhelpful; after 10 hrs they don't know where it is - it's not good enough @British_Airways",
    "⁦@KLM⁩ via Flying Blue kan ik enkel terugvliegen naar ⁦@Schiphol⁩, echter zou ik op de terugreis graag de KLM bus naar ⁦@EINairport⁩ willen. Kan dat door jullie vooraf of achteraf nog toegevoegd worden? Deze promo reward actie is nog maar tot vrijdag geldig. https://t.co/v0snpsOuNi"]
list_tail = ["@British_Airways Chrome. Same as I always use. Normally works fine. Very odd.",
             "@British_Airways Thank you. I appreciate the answer will remain the same. But I disagree with your method of misleading advertising and as I say will be logging a complaint with the ASA.",
             "@British_Airways Let me do so",
             "@British_Airways Thanks for this - just gotta work out what to for 5 hours now 🙂",
             "@British_Airways I was, why would i pay you €75 for the privilege of carrying my own bag? Your service at the best of times is atrocious. Still no response to my tweet from yesterday alerting you to baggage checkin issues. You're a total joke. Your boss @alex_cruz is pathetic.",
             "@British_Airways trying to understand options to change a booking. As I have waited so long have held another trip but this is due to expire",
             "@KLM Would lost and found have it if she left it in the seatback where magazines are located?",
             "@Klm should you already have if it is good, thanks again!",
             "@KLM No problem. Thanks for getting back to me so swiftly.", "@Klm a pity!",
             "@KLM Ok looks like I need to manage this though @Delta @DeltaAssist. Ball’s in your court. Thanks @KLM",
             "@KLM Dm sent 👍", "@Ryanair Will do thanks", "@Ryanair Thanks I just sent a DM 👍",
             "@Ryanair Ana, thank you so much for your help. Excellent customer service.",
             "@Ryanair Hello...I would like to cancel my booking OQVMUB  due to medical emergency. Request your kind support please",
             "@Ryanair Ok, so no. Thanks for the help.", "@Ryanair Sweet! Thanks for the quick reply!",
             "@Ryanair Thanks Ana I have DM but no response yet?", "@Ryanair I wrote the private message.",
             "@Ryanair so as long as the device is on flight mode?", "@Ryanair Thanks", "@Ryanair I havent",
             "@Ryanair Meri, did you get all the details I sent?",
             "@Ryanair Nah, found a workaround. If a passenger's registered passport has expired and they have a new one, the system doesn't allow you to change it at check-in, you have to go back into your account and update the details there.",
             "@KLM The next available flight is 24hrs later for a location in Europe. Many plans ruined because of your outright dishonesty.",
             "@lufthansa Perfect, thank you very much for the information.",
             "@lufthansa ok, great I finally got through.", "@lufthansa ok, great I finally got through.",
             "@lufthansa I keep going around in circles. When I go online thru the website, it lists my flights, and the first flight allowed me to book seats. For the second flight, from Munich to Rome, it says ,Seats not available at this time. I’m still trying to get around that.",
             "@lufthansa Ella, thank you for this, however is there a way a note can be put on the passengers profile so when they check-in they be provided at that time for an upgrade resulting from their treatment on the outbound segment. It is possible as it is done often, speaking from experience.",
             "@lufthansa They don't open the line until 7, my flight is at 9:50.",
             "@lufthansa While we're waiting still on standby and not anywhere closer to our destination they are selling upgrades but can't give us a seat... #areyouforreal #worstdayever #Lufthansaisthrworst",
             "@lufthansa Thanks!!", "@lufthansa But how much time it will take??",
             "@lufthansa I do not want to make any call. Why the did not respond to my email ??? Why you cant access my booking??? Why you cant answer my question?? My question very easy, why you cange my seat which i already choose and i paid money for reservations??",
             "@lufthansa I did call your support number and they said that they are aware of the issue...",
             "@lufthansa Unfortunately they have not even traced my bag yet... No urgency from them... I have been travelling for over 8 hours and now need to go shopping when I should be eating and sleeping ready for tomorrow. Not happy.",
             "@Ryanair dublin to cardiff",
             "@lufthansa I have a boarding pass that has a big fat Lufthansa logo on it. Is this just going to be you &amp; @united obfuscating responsibility for this issue?",
             "@British_Airways There are no members of staff here and no one has made an announcement. It’s typical evasion and avoidance. It’s now 35 minutes and nada. Later arrivals have had their bags delivered already. It’s pathetic.",
             "@KLM Okay, thanks!",
             "@KLM You miss the point. I dont understand. I accept flights are delayed; but i dont understand how your staff dont understand the benefits of certain memberships, nor can they do anything to mitigate the inconvenience",
             "@British_Airways I do hope so.  Thanks Tony ☺️",
             "@KLM Due to maintenance of the baggage claim, the suitcase probably did not come along. When I addressed the employee that I had to be sure whether the suitcase was going with me, I was informed that I was not his supervisor. 😤 result now known.",
             "@Ryanair Thanks for that, but the chat bot is advising me to contact the airport lost and found, which I have already done. Is there any other way for me to try get my jacket back, or is it gone for good?",
             "@British_Airways @HeathrowAirport Ugh, I’ll be watching this space closely because it needs to happen ASAP please. Thanks",
             "@lufthansa It is much later now.......... what’s going on?", "@KLM I have sent further information by DM",
             "@lufthansa @TravelLeisure @Carters @staralliance @united There weren’t many other folks flying Business so they let us expand our zone a bit. It worked out really well.🤩",
             "@lufthansa @RahulGandhi @priyankagandhi - Please help yourselves.... 😂😂",
             "@KLM Yes, the flight was good old-fashioned fun again. Friendly flight attendants...cozy fellow passengers. I'm already looking forward to Sunday when I fly with you again. #frequentflyer #FlyingBlue",
             "@British_Airways Yeah, the thing is y'all know where they are. You mad ethe choice to leave them behind. Which is baffling and infuriating.",
             "@British_Airways Have sent a DM Kev. Thanks",
             '@KLM Your "ground crew" was exceptional. Thank you for your help.  They saved the day with a short phone call. Thank you again',
             "@British_Airways I wish, we're getting off the plane at the moment, but to be fair the crew have done a decent job of keeping us informed...",
             "@British_Airways Yes I know, I fly almost every week. But you are not providing enough seats on the route. Sometimes your plans change at the last minute and even with a semi flexible ticket I was quoted £364 to change from morning to afternoon flight @RossThomson_MP",
             "@British_Airways BA 81 from London to Accra. This is an eyesore and a total waste of money.",
             "@Klm thank you!Really super nice.Tomorrow also the transfer of our house so it was really not possible a day before 🙈.",
             "@British_Airways How long does it take to get an update?? Surely the baggage is tagged so you should know EXACTLY where it is at any time? This is not reassuring"]
list_head_sent = ["Negative", "Negative", "Neutral", "Neutral", "Negative", "Negative", "Neutral", "Negative",
                  "Neutral", "Neutral", "Neutral", "Negative", "Neutral", "Neutral", "Neutral", "Neutral", "Neutral",
                  "Neutral", "Neutral", "Neutral", "Neutral", "Neutral", "Neutral", "Neutral", "Neutral", "Negative",
                  "Neutral", "Negative", "Negative", "Negative", "Neutral", "Negative", "Neutral", "Neutral",
                  "Negative", "Neutral", "Negative", "Neutral", "Neutral", "Negative", "Neutral", "Negative", "Neutral",
                  "Negative", "Neutral", "Neutral", "Negative", "Negative", "Positive", "Neutral", "Positive",
                  "Negative", "Negative", "Positive", "Negative", "Neutral", "Negative", "Positive", "Negative",
                  "Neutral"]
list_tail_sent = ["Positive", "Neutral", "Neutral", "Positive", "Negative", "Neutral", "Neutral", "Positive",
                  "Positive", "Negative", "Neutral", "Neutral", "Neutral", "Positive", "Positive", "Neutral", "Neutral",
                  "Positive", "Neutral", "Neutral", "Neutral", "Positive", "Neutral", "Neutral", "Neutral", "Negative",
                  "Positive", "Neutral", "Negative", "Positive", "Neutral", "Negative", "Positive", "Neutral",
                  "Negative", "Neutral", "Negative", "Neutral", "Neutral", "Negative", "Positive", "Negative",
                  "Positive", "Negative", "Negative", "Negative", "Negative", "Neutral", "Positive", "Neutral",
                  "Positive", "Negative", "Positive", "Positive", "Neutral", "Neutral", "Negative", "Positive",
                  "Negative", "Neutral"]

# CREATE DICTIONARIES WITH THE TWEET AND LABELED SENTIMENT FROM SAMPLE
dict_head = {}
count = 0
for el in list_head:
    dict_head[el] = list_head_sent[count]
    count += 1
print(dict_head)
dict_tail = {}
count = 0
for el in list_tail:
    dict_tail[el] = list_tail_sent[count]
    count += 1
print(dict_tail)

data = {'head_text': list_head, 'head_sentiment': list_head_sent, 'tail_text': list_tail, 'tail_sentiment': list_tail_sent} # gooi het in een df
df_sentiment_sample = pd.DataFrame.from_dict(data)

### sentiment analysis with algo from sample and get list with sentiments
count3 = 0
for el in list_head:
    sentiment_analysis(list_head[count3], list_tail[count3])
    count3 += 1

### compare the sentiments from the algo with the sentiments labeled
TF_head = sum(x == y for x, y in zip(list_head_sent, list_head_sent_algo))
TF_tail = sum(x == y for x, y in zip(list_tail_sent, list_tail_sent_algo))
p = ((TF_head + TF_tail) /(len(list_tail_sent)+len(list_head_sent))*100)
print(p)

TF_head_soepeler = sum(x == y or x == "Neutral" or y == "Neutral" for x, y in zip(list_head_sent, list_head_sent_algo))
TF_tail_soepeler = sum(x == y or x == "Neutral" or y == "Neutral"  for x, y in zip(list_tail_sent, list_tail_sent_algo))
p_soep = ((TF_head_soepeler + TF_tail_soepeler) /(len(list_tail_sent)+len(list_head_sent))*100)
print(p_soep)

### determine change in sentiment
threshold = 0.3

def determine_change(text1, text2): # retrns true of false if change in sentiment is present
    result = sentiment_analysis(text1, text2)
    is_more_pos = ((result[0]['Negative']-result[0]['Negative']*threshold) > result[1]['Negative']) and (result[0]['Neutral'] < result[1]['Neutral'] or result[0]['Positive'] < result[1]['Positive'])
    return result, is_more_pos

list_dict_sent = [] #sentiment dictionaries added for all tweets
list_bool_change = [] #TRUE or FALSE added for all tweets if change in sentiment is present
head_pos = []
head_neg = []
head_neu = []
tail_pos = []
tail_neg = []
tail_neu = []


import sqlite3
import pandas as pd
from SQLITE_Queries import *
conn = sqlite3.connect('DataChallenge.sqlite')
cursor = conn.cursor()
query_all = cursor.execute('SELECT * FROM main.KLM;').fetchall()  # main.airline depending on what airline you want to analyse
for row in query_all:
    head_tweet = row[1]
    tail_tweet = row[3]
    bool_change = determine_change(head_tweet, tail_tweet)
    list_dict_sent.append(bool_change[0])
    head_neg.append(bool_change[0][0]['Negative'])
    head_neu.append(bool_change[0][0]['Neutral'])
    head_pos.append(bool_change[0][0]['Positive'])
    tail_neg.append(bool_change[0][1]['Negative'])
    tail_neu.append(bool_change[0][1]['Neutral'])
    tail_pos.append(bool_change[0][1]['Positive'])
    list_bool_change.append(bool_change[1])

df_sent = pd.DataFrame({'Sentiment Dictionary':list_dict_sent, 'Sentiment Positively Changed':list_bool_change})

df_sent_with_values = pd.DataFrame({'Sentiment Dictionary':list_dict_sent, 'Sentiment Positively Changed':list_bool_change, 'Neg head':head_neg, 'Neu head':head_neu, 'Pos head':head_pos, 'Neg tail':tail_neg, 'Neu tail':tail_neu, 'Pos tail':tail_pos})

