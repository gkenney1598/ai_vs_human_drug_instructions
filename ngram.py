import random
import nltk
from nltk.util import ngrams
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification

def jaccard_distance(a, b):
    """Calculate the Jaccard distance between sets A and B"""
    a = set(a)
    b = set(b)
    return 1.0 * len(a & b) / len(a | b)

df = pd.read_csv("data/Human_ChatGPTGen.csv")

df = df.rename(columns={"instructions": "sentence", "generated": "labels"})

similarity_score = 0
for i in range(500):
    sentence1 = df.iloc[i, 1]
    human_words = nltk.word_tokenize(sentence1)
    sentence2 = df.iloc[i+500, 1]
    chat_words = nltk.word_tokenize(sentence2)
    
    humangrams = list(ngrams(human_words, 10))
    chatgrams = list(ngrams(chat_words, 10))

    similarity_score += jaccard_distance(humangrams, chatgrams)
print("Average Similarity Score: ", similarity_score/500)

