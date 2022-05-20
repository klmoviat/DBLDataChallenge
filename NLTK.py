# lookt at nr tweets per hour per person

import nltk
#nltk.download()

"""
words = [w for w in nltk.corpus.state_union.words() if w.isalpha()] # no puntuation, capital sensible
stopwords = nltk.corpus.stopwords.words("english") # when exactly is a word a stopword?
words = [w for w in words if w.lower() not in stopwords] # only remove lowercase as only lowercase was in stopwords list


#make own list of words from text with nltk.word_tokenize(), a function that splits raw text into individual words:
from pprint import pprint
textt = 'BREAKING:-\nKLM to fly 3x weekly btw @BLRAirport and @Schiphol from winter schedule 2018/19 using Boeing 787-9 aircr… https://t.co/XazlSBalNv'
pprint(nltk.word_tokenize(textt), width=79, compact=True) # vaag van de site
print([w for w in nltk.word_tokenize(textt) if w.isalpha()]) # zelf+ alleen letters

#frequancy distributions
#words = nltk.word_tokenize(text)
fd = nltk.FreqDist(words) #like dict of frequencies but with added features
fd.most_common(3)
fd.tabulate(3) #table
lower_fd = nltk.FreqDist([w.lower() for w in fd]) # makes all words lowercase

# concordances: How many times a word appears, Where each occurrence appears, What words surround each occurrence
text = nltk.Text(nltk.corpus.state_union.words()) # case insensitive
text.concordance("america", lines=5) #Displaying 5 of 1079 matches
concordance_list = text.concordance_list("america", lines=2) #sorted in appearance

words = [w for w in nltk.corpus.state_union.words() if w.isalpha()]
finder = nltk.collocations.TrigramCollocationFinder.from_words(words) #Bigrams: Frequent two-word combinations, Trigrams: Frequent three-word combinations, Quadgrams: Frequent four-word combinations
finder.ngram_fd.most_common(2) # find 2 most common collocations
finder.ngram_fd.tabulate(2)
"""

# VADER = NLTK's sentiment analyzer, best suited for language used in social media (short sentences, slang, abbreviations). less accurate when rating longer, structured sentences, but it’s often a good launching point. To get better results, you’ll set up VADER to rate individual sentences within the review rather than the entire text.
#
#

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
a = sia.polarity_scores("Wow, NLTK is really powerful!") #polarity scores, The negative, neutral, and positive scores are related: They all add up to 1 and can’t be negative. The compound score is not just an average, and it can range from -1 to 1
print(a)

tweets = [t.replace("://", "//") for t in nltk.corpus.twitter_samples.strings()] #load the twitter_samples corpus into a list of strings, making a replacement to render URLs inactive to avoid accidental clicks
from random import shuffle

#classify tweets
def is_positive(tweet: str) -> bool:
    """True if tweet has positive compound sentiment, False otherwise."""
    return sia.polarity_scores(tweet)["compound"] > 0

shuffle(tweets)
for tweet in tweets[:10]:
    print(">", is_positive(tweet), tweet)

# already classified movie reviews to judge accuracy of algo's
positive_review_ids = nltk.corpus.movie_reviews.fileids(categories=["pos"])
negative_review_ids = nltk.corpus.movie_reviews.fileids(categories=["neg"])
all_review_ids = positive_review_ids + negative_review_ids

# work on an entire review
from statistics import mean

def is_positive(review_id: str) -> bool:
    """True if the average of all sentence compound scores is positive."""
    text = nltk.corpus.movie_reviews.raw(review_id) # ever ID has 1 review
    scores = [
        sia.polarity_scores(sentence)["compound"]
        for sentence in nltk.sent_tokenize(text) # create list of sentences from review
    ]
    return mean(scores) > 0

# test accuracy, with predefined pos and neg cases, this algo has 64% accuracy.
#
#

shuffle(all_review_ids)
correct = 0
for review_id in all_review_ids: # all_review_ids = positive_review_ids + negative_review_ids
    if is_positive(review_id):
        if review_id in positive_review_ids:
            correct += 1
    else:
        if review_id in negative_review_ids:
            correct += 1

print(F"{correct / len(all_review_ids):.2%} correct")

# customizing NLTK's sentiment analysis
#
#

#exclude unwanted words+ build category groups
unwanted = nltk.corpus.stopwords.words("english")
unwanted.extend([w.lower() for w in nltk.corpus.names.words()]) # dont want actor's names

def skip_unwanted(pos_tuple):
    word, tag = pos_tuple
    if not word.isalpha() or word in unwanted:
        return False
    if tag.startswith("NN"):
        return False
    return True

positive_words = [word for word, tag in filter(
    skip_unwanted,
    nltk.pos_tag(nltk.corpus.movie_reviews.words(categories=["pos"])))]
negative_words = [word for word, tag in filter(
    skip_unwanted,nltk.pos_tag(nltk.corpus.movie_reviews.words(categories=["neg"])))]

# find set words pos and neg have in common+ remove it from pos and neg
positive_fd = nltk.FreqDist(positive_words)
negative_fd = nltk.FreqDist(negative_words)

common_set = set(positive_fd).intersection(negative_fd)

for word in common_set:
    del positive_fd[word]
    del negative_fd[word]

top_100_positive = {word for word, count in positive_fd.most_common(100)}
top_100_negative = {word for word, count in negative_fd.most_common(100)} # but still have uncommon names and words that aren’t necessarily positive or negative

# add leverage for more pos and neg bigrams
unwanted = nltk.corpus.stopwords.words("english")
unwanted.extend([w.lower() for w in nltk.corpus.names.words()])

positive_bigram_finder = nltk.collocations.BigramCollocationFinder.from_words([
    w for w in nltk.corpus.movie_reviews.words(categories=["pos"])
    if w.isalpha() and w not in unwanted
])
negative_bigram_finder = nltk.collocations.BigramCollocationFinder.from_words([
    w for w in nltk.corpus.movie_reviews.words(categories=["neg"])
    if w.isalpha() and w not in unwanted
])

# training and using a classifier
#
#

# extract features for each piece of text:
# 1. The average compound score
# 2. The average positive and negative score
# 3. The amount of words in the text that are also part of the top 100 words in all positive reviews
def extract_features(text):
    features = dict()
    wordcount = 0
    wordcount2 = 0
    compound_scores = list()
    positive_scores = list()
    negative_scores = list()

    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            if word.lower() in top_100_positive:
                wordcount += 1
            if word.lower() in top_100_negative:
                wordcount2 += 1
        compound_scores.append(sia.polarity_scores(sentence)["compound"])
        positive_scores.append(sia.polarity_scores(sentence)["pos"])
        negative_scores.append(sia.polarity_scores(sentence)["neg"])

    # Adding 1 to the final compound score to always have positive numbers
    # since some classifiers you'll use later don't work with negative numbers.
    features["mean_compound"] = mean(compound_scores) + 1
    features["mean_positive"] = mean(positive_scores)
    features["mean_negative"] = mean(negative_scores)
    features["wordcount"] = wordcount

    return features

# build a list of features for each text you’ll analyze, first item is the dictionary returned by extract_features and whose second item is the predefined category for the text
features = [
    (extract_features(nltk.corpus.movie_reviews.raw(review)), "pos")
    for review in nltk.corpus.movie_reviews.fileids(categories=["pos"])
]
features.extend([
    (extract_features(nltk.corpus.movie_reviews.raw(review)), "neg")
    for review in nltk.corpus.movie_reviews.fileids(categories=["neg"])
])

# classify new data
# Use 1/4 of the set for training
train_count = len(features) // 4
shuffle(features)
classifier = nltk.NaiveBayesClassifier.train(features[:train_count])
classifier.show_most_informative_features(10)
nltk.classify.accuracy(classifier, features[train_count:])

new_review = 'BREAKING:-\nKLM to fly 3x weekly btw @BLRAirport and @Schiphol from winter schedule 2018/19 using Boeing 787-9 aircr… https://t.co/XazlSBalNv'
classifier.classify(new_review)
extract_features(new_review)

# additional classifiers with scikit-learn
#
#

from sklearn.naive_bayes import (
    BernoulliNB,
    ComplementNB,
    MultinomialNB,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

classifiers = {
    "BernoulliNB": BernoulliNB(),
    "ComplementNB": ComplementNB(),
    "MultinomialNB": MultinomialNB(),
    "KNeighborsClassifier": KNeighborsClassifier(),
    "DecisionTreeClassifier": DecisionTreeClassifier(),
    "RandomForestClassifier": RandomForestClassifier(),
    "LogisticRegression": LogisticRegression(),
    "MLPClassifier": MLPClassifier(max_iter=1000),
    "AdaBoostClassifier": AdaBoostClassifier(),
}

# Use 1/4 of the set for training
train_count = len(features) // 4
shuffle(features)
for name, sklearn_classifier in classifiers.items():
    classifier = nltk.classify.SklearnClassifier(sklearn_classifier)
    classifier.train(features[:train_count])
    accuracy = nltk.classify.accuracy(classifier, features[train_count:])
    print(F"{accuracy:.2%} - {name}")

