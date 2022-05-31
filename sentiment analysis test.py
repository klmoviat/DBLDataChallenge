# sentiment analysis algo
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
# analyse 1st Tweet
text = "It was absolutely fucking terrible trash, would not recommend. :("
text = preprocess(text)
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)
scores = output[0][0].detach().numpy()
scores = softmax(scores)
ranking = np.argsort(scores)
ranking = ranking[::-1]
for i in range(scores.shape[0]):
    l = config.id2label[ranking[i]]
    s = scores[ranking[i]]
    print(f"{i+1}) {l} {np.round(float(s), 4)}")

# analyse 2nd Tweet
text2 = "It was absolutely super amazing awesome, would absolutely recommend. :)"
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
    print(f"{i+1}) {l} {np.round(float(s), 4)}")

# create dictionaries with the sentiment scores of the 1st and 2nd Tweet
dict = {}
for i in range(3):
    dict['negative'] = scores[0]
    dict['neutral'] = scores[1]
    dict['positive'] = scores[2]
dict2 = {}
for i in range(3):
    dict2['negative'] = scores2[0]
    dict2['neutral'] = scores2[1]
    dict2['positive'] = scores2[2]

# compare the positive and neg semantic analysis
max_val = list(dict.values())
max_ke = list(dict.keys())
tuple1 = (max_ke[max_val.index(max(max_val))], max(max_val)) # a tuple of the highest sentiment and score
max_val2 = list(dict2.values())
max_ke2 = list(dict2.keys())
tuple2 = (max_ke2[max_val2.index(max(max_val2))], max(max_val2))

# calculate sentiment change (the difference in positive score)
delta = (dict['positive'] - dict2['positive'])
print(f"difference is {delta} (positive before={dict['positive']}, positive after={dict2['positive']})")

