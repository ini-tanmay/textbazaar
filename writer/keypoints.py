import nltk
from nltk.tokenize import sent_tokenize
import pandas as pd
import networkx as nx
import numpy as np
from nltk.corpus import stopwords
import os
from django.conf import settings
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
    
def summarize(query,email):
    contents=get_contents(query)
    no_of_lines=30
    clean_sentences,sentences=clean_all_sentences(contents)
    word_embeddings=extract_word_vectors()
    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((50,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((50,))
        sentence_vectors.append(v)
    # similarity matrix
    sim_mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,50), sentence_vectors[j].reshape(1,50))[0,0]
       #textrank 
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    # Extract top n sentences as the summary
    if len(ranked_sentences)<30:
        no_of_lines=len(ranked_sentences)
    summary=''
    for i in range(no_of_lines):
      summary+=ranked_sentences[i][1]+' %0A '
    # user=User.objects.filter(email=email)
    # article=Article(user=user,title='KeyPoints: %0A'+query,content=summary)
    # article.save()
    # user.update(credits_used=F('credits_used') + 1)  
    send_email('This is a summary', summary, email)    
    return 'done'  