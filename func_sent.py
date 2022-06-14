from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
from progressbar import ProgressBar
import numpy as np


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


def sentiment_analysis(text1, text2, conv_id):
    # analyse 1st Tweet
    text1 = preprocess(text1)

    encoded_input = tokenizer(text1, return_tensors='pt')
    output = model(**encoded_input) #deze statement duurt relatief lang
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # analyse 2nd Tweet
    text2 = preprocess(text2)
    encoded_input2 = tokenizer(text2, return_tensors='pt')
    output2 = model(**encoded_input2)
    scores2 = output2[0][0].detach().numpy()
    scores2 = softmax(scores2)
    first = (-1*scores[0]+scores[2])/2+0.5
    last = (-1*scores2[0]+scores2[2])/2+0.5
    return first, last, last - first, conv_id


def sentiment_analysis_nl(text1, text2, conv_id):
    # analyse 1st Tweet
    text1 = preprocess(text1)

    encoded_input = tokenizer_nl(text1, return_tensors='pt')
    output = model_nl(**encoded_input) #deze statement duurt relatief lang
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # analyse 2nd Tweet
    text2 = preprocess(text2)
    encoded_input2 = tokenizer_nl(text2, return_tensors='pt')
    output2 = model_nl(**encoded_input2)
    scores2 = output2[0][0].detach().numpy()
    scores2 = softmax(scores2)
    first = (-1*scores[0]+scores[2])/2+0.5
    last = (-1*scores2[0]+scores2[2])/2+0.5
    return first, last, last - first, conv_id


def sentiment_compare(before, after, conv_id):
    all_scores = []
    pbar = ProgressBar()
    for x in pbar(range(len(before))):
        score = sentiment_analysis(before[x], after[x], conv_id[x])
        all_scores.append(score)
    pbar.finish()
    return all_scores


def sentiment_compare_nl(before, after, conv_id):
    all_scores = []
    # Sentiment analysis stuffings
    pbar = ProgressBar()
    for x in pbar(range(len(before))):
        score = sentiment_analysis_nl(before[x], after[x], conv_id[x])
        all_scores.append(score)
    pbar.finish()
    return all_scores


def add_sentiment(table, conn, cursor):
    head_temp = cursor.execute("SELECT head_text, CONV_ID from " + table +
                               " inner join main on head = id_str where lang = 'en'").fetchall()
    head = [i[0] for i in head_temp]
    conv_id = [i[1] for i in head_temp]
    tail_temp = cursor.execute("SELECT tail_text from " + table +
                               " inner join main on head = id_str where lang = 'en'").fetchall()
    tail = [i[0] for i in tail_temp]
    if table == 'KLM':
        head_nl_temp = cursor.execute("SELECT head_text, CONV_ID from " + table +
                                      " inner join main on head = id_str where lang = 'nl'").fetchall()
        head_nl = [i[0] for i in head_nl_temp]
        conv_id_nl = [i[1] for i in head_nl_temp]
        tail_nl_temp = cursor.execute("SELECT tail_text from " + table +
                                      " inner join main on head = id_str where lang = 'nl'").fetchall()
        tail_nl = [i[0] for i in tail_nl_temp]
        result = sentiment_compare(head, tail, conv_id) + sentiment_compare_nl(head_nl, tail_nl, conv_id_nl)
    else:
        result = sentiment_compare(head, tail, conv_id)
    cursor.execute("ALTER TABLE " + table + " add head_sentiment")
    cursor.execute("ALTER TABLE  " + table + "  add tail_sentiment")
    cursor.execute("ALTER TABLE  " + table + "  add delta_sentiment")
    cursor.executemany("UPDATE  " + table + "  SET head_sentiment = (?), tail_sentiment = (?),"
                                            " delta_sentiment = (?) where CONV_ID = (?)", result)
    conn.commit()
