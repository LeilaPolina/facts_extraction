# -*- coding: utf-8 -*-

import os
import re

vvodn_path = os.path.dirname(os.path.abspath(__file__)) + '/vvodn/'

special_constr1 = re.compile(u"^как сообщает \w+,", flags = re.I + re.U)
special_constr2 = re.compile(u"^как сообщается \w+,", flags = re.I + re.U)

def cut_special_constr(sentence):
    check = False
    if len(re.findall(special_constr1, sentence)) > 0 or len(re.findall(special_constr2, sentence)) > 0:
        check = True
    return check

def count_words(string):
    tokens = string.split()
    return len(tokens)
	
def cut_vvodn(sentence, vvodn_list, target_part, end_part):
    target_part = target_part.lower()
    for word in vvodn_list:
        if target_part == word.decode('utf-8'):
            end_part = end_part[:1].upper() + end_part[1:]
            sentence = end_part
            return sentence
    return sentence

def search_vvodn(sentence, n_words, target_part, end_part):
    vvodn = []
    if n_words == 1:
        with open(vvodn_path + 'one_word_vvodn.txt', "r") as vfile:
            vvodn = vfile.read()            
    elif n_words == 2:
        with open(vvodn_path + 'two_word_vvodn.txt', "r") as vfile:
            vvodn = vfile.read()
    elif n_words == 3:
        check = False
        check = cut_special_constr(sentence)
        if check == True:
            sentence = end_part
            return sentence
        with open(vvodn_path + 'three_word_vvodn.txt', "r") as vfile:
            vvodn = vfile.read()
    elif n_words == 4:
        with open(vvodn_path + 'four_word_vvodn.txt', "r") as vfile:
            vvodn = vfile.read()
    else:
        with open(vvodn_path + 'five_word_vvodn.txt', "r") as vfile:
            vvodn = vfile.read()            
    lines = vvodn.split('\n')
    sentence = cut_vvodn(sentence, lines, target_part, end_part)
    return sentence

def filter_vvodn(sentence, result_text):
    vvodn = sentence.split(', ', 1)
    check_full = vvodn[0][-1] != '.' and vvodn[0][-1] != '!' and vvodn[0][-1] != '?'
    if check_full:           
        n_words = count_words(vvodn[0])
        if n_words < 6:
            sentence = search_vvodn(sentence, n_words, vvodn[0], vvodn[1])
            result_text.append(sentence)
        else:
            result_text.append(sentence)
    else:
        result_text.append(sentence)
        
    return result_text