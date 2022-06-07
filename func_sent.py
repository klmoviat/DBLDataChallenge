from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
import numpy as np


# Sentiment analysis stuffings
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
# MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"
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

    # create dictionaries with the sentiment scores of the 1st and 2nd Tweet
    # dict = {}
    # for i in range(3):
    #     dict['Negative'] = scores[0]
    #     dict['Neutral'] = scores[1]
    #     dict['Positive'] = scores[2]
    # dict2 = {}
    # for i in range(3):
    #     dict2['Negative'] = scores2[0]
    #     dict2['Neutral'] = scores2[1]
    #     dict2['Positive'] = scores2[2]
    # # compare the positive and neg semantic analysis
    # max_val = list(dict.values())  ### THIS IS THE SENTIMENT BEFORE ACCORDING TO THE ALGO
    # max_ke = list(dict.keys())
    # tuple1 = (max_ke[max_val.index(max(max_val))], max(max_val))  # a tuple of the highest sentiment and score
    # max_val2 = list(dict2.values())
    # max_ke2 = list(dict2.keys())
    # tuple2 = (max_ke2[max_val2.index(max(max_val2))], max(max_val2))
    first = (-1*scores[0]+scores[2])/2+0.5
    last = (-1*scores2[0]+scores2[2])/2+0.5
    return first, last, last - first, conv_id
    #return [resulting(max_ke[max_val.index(max(max_val))]), resulting(max_ke2[max_val2.index(max(max_val2))]),
            #resulting(max_ke2[max_val2.index(max(max_val2))]) - resulting(max_ke[max_val.index(max(max_val))])]

    # calculate sentiment change (the difference in positive score)
    # delta = (dict['positive'] - dict2['positive'])
    # print(f"difference is {delta} (positive before={dict['positive']}, positive after={dict2['positive']})")


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

    # create dictionaries with the sentiment scores of the 1st and 2nd Tweet
    # dict = {}
    # for i in range(3):
    #     dict['Negative'] = scores[0]
    #     dict['Positive'] = scores[1]
    # dict2 = {}
    # for i in range(3):
    #     dict2['Negative'] = scores2[0]
    #     dict2['Positive'] = scores2[1]
    first = (-1*scores[0]+scores[2])/2+0.5
    last = (-1*scores2[0]+scores2[2])/2+0.5
    return first, last, last - first, conv_id


def sentiment_compare(before, after, conv_id):
    all_scores = []
    for x in range(len(before)):
        score = sentiment_analysis(before[x], after[x], conv_id[x])
        all_scores.append(score)
    return all_scores


def sentiment_compare_nl(before, after, conv_id):
    all_scores = []
    # Sentiment analysis stuffings
    for x in range(len(before)):
        score = sentiment_analysis_nl(before[x], after[x], conv_id[x])
        all_scores.append(score)
    return all_scores
