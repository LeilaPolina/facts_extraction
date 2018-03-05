# -*- coding: utf-8 -*-

import os
import json
import nltk.data

import vvodn_words
import dir_speech

news_path = os.path.dirname(os.path.abspath(__file__)) + '/malt_news_json/'

def begin_filter(article):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(article)
    result_text = []
    result_text_dir = []
    result_text_vvodn = []
    # два цикла необходимы потому, что в поиске прямой речи приходится возвращаться
    # к прошлым предложениям, а вводные слова лучше искать когда лишние кавычки уже удалены
    for index, sentence in enumerate(sentences):
        sentence = sentence.replace(".".decode('utf-8'), "_".decode('utf-8'))
        sentence = sentence.replace("»".decode('utf-8'), "\"".decode('utf-8'))
        sentence = sentence.replace("«".decode('utf-8'), "\"".decode('utf-8'))
        result_text_dir = dir_speech.filter_dir_speech(sentence, index, result_text_dir)
    
    for sentence in result_text_dir:
        result_text_vvodn = vvodn_words.filter_vvodn(sentence, result_text_vvodn)
    
    result_text = result_text_vvodn
    
    result_text = ' '.join(result_text)
    return result_text

def filter_one(): #FOR JUST ONE FILE 
    fname = news_path + '13.json'    
    with open(fname, "r") as json_file:
        data = json.load(json_file, strict = False)
        
    article = data['description']
    article = begin_filter(article)    
    article = article.encode('utf-8')
    print article
    data['description'] = article
    #data['pubDate'] = data['pubDate'].encode('utf-8')
    data['title'] = data['title'].encode('utf-8')
    #print data['description']
    """
    with open(fname, "w") as json_file:
        json.dump(data, json_file, ensure_ascii = False, indent = 1, sort_keys = True)
    print("\nsuccessfully filtered!").upper()
    """
    
def filter_all():#FOR ALL FILES IN THE DIRECTORY
    for filename in os.listdir(news_path):
        if filename.endswith(".json"):
            fname = news_path + filename
            print filename
            with open(fname, "r") as json_file:
                data = json.load(json_file, strict = False)
            article = data['description']
            article = begin_filter(article)
            article = article.encode('utf-8')
            data['description'] = article
            #data['pubDate'] = data['pubDate'].encode('utf-8')
            data['title'] = data['title'].encode('utf-8')
            with open(fname, "w") as json_file:
                json.dump(data, json_file, ensure_ascii = False, indent = 1, sort_keys = True)
    print("\nsuccessfully filtered!").upper()
    
filter_one()