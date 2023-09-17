# remove HTML tags 
#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8


import logging
from flask import Flask, jsonify, request

import pickle

# from nltk.tokenize import  word_tokenizen 
from bs4 import BeautifulSoup
import lxml
import os
import html5lib
import tensorflow_hub as hub
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
import pickle as cPickle
import gzip 



#  Chargement du modele
# with open("usemodel.pkl", "rb") as f:
#     model = pickle.load(f)

# test1 = pickle.dumps(model, protocol=0)
# test2 = pickle.dumps(model, protocol=-1)
# test2 = pickle.dumps(model, protocol=-1)
# from sys import getsizeof
# size_old = getsizeof(test1)
# size_new = getsizeof(test2)
# print(size_old, size_new)

# with gzip.open('test_zip','wb') as f:
#     cPickle.dump(model, f, protocol=-1)

# getsizeof(model)

# test3 = pickle.dumps(modeltest, protocol=-1)
# size_new2 = getsizeof(test3)
# print(size_new2)
# size_new2 = getsizeof(test3)
# print(size_new2)

# with gzip.open('test_zip','wb') as f:
#      test4 = cPickle.dump(model, f, protocol=-1)
 
# size_new2 = getsizeof(test4)
# print(size_new2)

# with gzip.open('usemodel','wb') as f:
#     cPickle.dump(model, f, protocol=-1)




app = Flask(__name__)
@app.route("/tag_prediction", methods=["POST"])
def predict_tag():
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
# Recuperer les donnees de la requete
    print('je suis entrée')
    data = request.get_json()
    question = data["question"]
    print('question' + question)

    preprocessed_question = preprocess(question)
    embeded_question = embed([preprocessed_question])
    with gzip.open("use_model", "rb") as f:
        model = cPickle.load(f)
    predicted_tags = model.predict([embeded_question])
    # Conversion des tags en liste
    predicted_tags_list = predicted_tags.tolist()

    # Appliquer le seuil de 0.5 pour obtenir des valeurs de 0 ou 1
    df_thresholded = predicted_tags >= 0.5
    targets = pd.read_csv('targets.csv')
    
    target_names = list(targets['target'])
    result = pd.DataFrame(df_thresholded, columns=target_names).T
    prediction = list(result[result[0] == True].index)
    return jsonify({"tags": prediction})



def preprocess(text):
    # Effectuer le pretraitement du texte (ex : suppression des stopwords, normalisation, etc.)
    # Retourner le texte pretraite
    desc_text = clean_text(text)
    word_tokens = tokenizer_fct(desc_text)
#    sw = stop_word_filter_fct(word_tokens)
    lw = lower_start_fct(word_tokens)
    # lw_noun = keep_nouns(lw)
    # lem_w = lemma_fct(lw)    
    transf_desc_text = ' '.join(lw)
    return transf_desc_text
    return text

def tokenizer_fct(sentence) :
    # sentence_clean = re.sub('[;(),\.!?]', '', sentence)
    sentence_clean = sentence.replace('.', ' . ').replace('?', ' ? ').replace('!', ' ! ').replace(';', ' ; ').replace(',', ' , ').replace('[', ' [ ').replace(']', ' ] ').replace(':', ' : ').replace('(', ' ( ').replace(')', ' ) ').replace('+', ' + ').replace('...', ' ... ').replace('\n', ' ')
    word_tokens = word_tokenize(sentence_clean)
    return word_tokens

def clean_text (text):
    soup = BeautifulSoup(text, "html5lib")

    for sentence in soup(['style' , 'script']):
        sentence.decompose()

    return ' '.join(soup.stripped_strings)

def lower_start_fct(list_words) :
    lw = [w.lower() for w in list_words]
    return lw

if __name__ == "__main__":
    # app.run(debug=True,host='0.0.0.0',port=os.environ.get("PORT", 8000))
    app.run(debug=True)

    # une fois les tests realise, enregistrer le modele bagofwords en utilisant pickle, et le charger ici et l'utiliser pour predire les tags


