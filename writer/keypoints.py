from nltk.tokenize import sent_tokenize
import pandas as pd
import networkx as nx
import numpy as np
from nltk.corpus import stopwords
import os
from django.conf import settings
import nltk
# from background_task import background
from .email import *
from sklearn.metrics.pairwise import cosine_similarity
from .helpers import * 

def extract_word_vectors():
    word_embeddings = {}
    f1= open(os.path.join(settings.BASE_DIR, 'glove.6B.50d.1.txt'),encoding='utf-8')
    for line in f1:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f1.close()
    f2= open(os.path.join(settings.BASE_DIR, 'glove.6B.50d.2.txt'),encoding='utf-8')
    for line in f2:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f2.close()        
    return word_embeddings

# function to remove stopwords
def remove_stopwords(sen):
    stop_words = stopwords.words('english')
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

def clean_all_sentences(contents):
    sentences = []
    for text in contents:
      sentences.append(sent_tokenize(text))

    sentences = [y for x in sentences for y in x] # flatten list
    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

    # make alphabets lowercase
    clean_sentences = [s.lower() for s in clean_sentences]
    # remove stopwords from the sentences
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    return clean_sentences,sentences
    
