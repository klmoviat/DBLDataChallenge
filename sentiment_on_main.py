import sqlite3
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification

from datetime import datetime


conn = sqlite3.connect("D:\\EXPORT\\ALL_DATA.sqlite")
cursor = conn.cursor()
# Sentiment analysis stuffings
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)


# dutch sentiment analysis
MODEL_nl = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"
tokenizer_nl = AutoTokenizer.from_pretrained(MODEL_nl)
config_nl = AutoConfig.from_pretrained(MODEL_nl)
model_nl = AutoModelForSequenceClassification.from_pretrained(MODEL_nl)



def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def single_sentiment(tweet, id_str):
    text1 = preprocess(tweet)
    encoded_input = tokenizer(text1, return_tensors='pt')
    output = model(**encoded_input)  # deze statement duurt relatief lang
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    score = (-1 * scores[0] + scores[2]) / 2 + 0.5
    return score, id_str


def single_sentiment_nl(tweet, id_str):
    text1 = preprocess(tweet)
    encoded_input = tokenizer_nl(text1, return_tensors='pt')
    output = model_nl(**encoded_input)  # deze statement duurt relatief lang
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    score = (-1 * scores[0] + scores[2]) / 2 + 0.5
    return score, id_str


info = cursor.execute("""SELECT m.id_str, text, lang from main.main m
left join replies r on m.id_str = r.in_reply_to_status_id_str
where r.in_reply_to_status_id_str is NULL AND
    (user_mentions like 'KLM' or user_mentions like '% KLM'
   or user_mentions like 'KLM, %' or user_mentions like '% KLM,%') and text not like 'RT %'
UNION
SELECT m.id_str, text, lang from main.main m
left join replies r on m.id_str = r.in_reply_to_status_id_str
where r.in_reply_to_status_id_str is NULL AND
    (user_mentions like 'British_Airways' or user_mentions like '% British_Airways'
   or user_mentions like 'British_Airways, %' or user_mentions like '% British_Airways,%') and text not like 'RT %'
UNION
SELECT m.id_str, text, lang from main.main m
left join replies r on m.id_str = r.in_reply_to_status_id_str
where r.in_reply_to_status_id_str is NULL AND
    (user_mentions like 'RyanAir' or user_mentions like '% RyanAir'
   or user_mentions like 'RyanAir, %' or user_mentions like '% RyanAir,%') and text not like 'RT %'
UNION
SELECT m.id_str, text, lang from main.main m
left join replies r on m.id_str = r.in_reply_to_status_id_str
where r.in_reply_to_status_id_str is NULL AND
    (user_mentions like 'Lufthansa' or user_mentions like '% Lufthansa'
   or user_mentions like 'Lufthansa, %' or user_mentions like '% Lufthansa,%') and text not like 'RT %';""").fetchall()
tweet = [i[1] for i in info]
id_str = [i[0] for i in info]
language = [i[2] for i in info]
all_scores = []
for x in range(len(tweet)):
    if language[x] == 'en':
        try:
            score = single_sentiment(tweet[x], id_str[x])
            all_scores.append(score)
        except RuntimeError:
            pass
    elif language[x] == 'nl':
        try:
            score = single_sentiment_nl(tweet[x], id_str[x])
            all_scores.append(score)
        except RuntimeError:
            pass
    print(str(x/len(tweet)*100) + '%')
    print(x)
print(datetime.now())
cursor.execute("create table 'temp' as select (?) as sentiment, (?) as id", all_scores)
