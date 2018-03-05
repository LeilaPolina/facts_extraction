# -*- coding: utf-8 -*-

import re

punct_sign_1 = "\", — ".decode('utf-8')
punct_sign_2 = "\", - ".decode('utf-8')

open_sign_regex = re.compile(u"\"[а-яА-ЯёЁa-zA-Z0-9]\w+", flags = re.I + re.U)
reversed_open_sign_regex = re.compile(u"[а-яА-ЯёЁa-zA-Z0-9]\w+\"", flags = re.I + re.U)

close_sign_1 = "\" ".decode('utf-8')
close_sign_2 = "\".".decode('utf-8')
close_sign_3 = "\"!".decode('utf-8')
close_sign_4 = "\"?".decode('utf-8')
close_sign_5 = "\",".decode('utf-8')
    
def filter_dir_speech(sentence, index, result_text):
    check_1 = sentence.find(punct_sign_1) != -1
    check_2 = sentence.find(punct_sign_2) != -1    
    direct_speech_true = check_1 or check_2
    
    if direct_speech_true:
        dir_speech = ['', '']
        if check_1:                
            dir_speech = sentence.split(punct_sign_1, 1)
        elif check_2:
            dir_speech = sentence.split(punct_sign_2, 1)
        
        sentence_chunk = dir_speech[0] + '.'
        
        open_signs_num = count_open_signs(sentence_chunk)
        close_signs_num = 1 + count_close_signs(sentence_chunk)
        
        # IF DIRECT SPEECH STARTS AND ENDS IN ONE SENTENCE
        if open_signs_num == close_signs_num:
            result_text = search_one_sentence(open_signs_num, sentence_chunk, result_text)
            
        # IF DIRECT SPEECH STARTS IN ANOTHER SENTENCE
        elif open_signs_num < close_signs_num:
            result_text = search_previous_sentences(open_signs_num, index, sentence_chunk, result_text)
            
        # IF SMTH UNEXPECTED HAPPENED
        else:
            print "what is this?".upper()
            print sentence_chunk
    else:
         result_text.append(sentence)
    
    return result_text

def count_open_signs(sentence):
    num = re.findall(open_sign_regex, sentence)
    num = len(num)
    return num

def count_close_signs(sentence):
    num = sentence.count(close_sign_1) + sentence.count(close_sign_2) + sentence.count(close_sign_3) + sentence.count(close_sign_4) + sentence.count(close_sign_5)
    return num

def wslash_open_sign_ind(sentence_chunk):    
    reverse_chunk = sentence_chunk[::-1]
    raw_matches = re.finditer(reversed_open_sign_regex, reverse_chunk)
    matches = []
    for raw_match in raw_matches:
        matches.append(raw_match)
    
    return - matches[0].end(0)

def search_one_sentence(open_signs_num, sentence_chunk, result_text):
    if open_signs_num == 1:
        open_sign_ind = wslash_open_sign_ind(sentence_chunk) + 1
        sentence_chunk = sentence_chunk[open_sign_ind:]
        result_text.append(sentence_chunk)
    else:
        new_sentence = search_beginning(sentence_chunk)
        result_text.append(new_sentence)
    return result_text

def find_last_close_sign(sentence):
    close_ind = sentence.rfind(close_sign_1)
    if(close_ind == -1):
        close_ind = sentence.rfind(close_sign_2)
        if(close_ind == -1):
            close_ind = sentence.rfind(close_sign_3)
            if(close_ind == -1):
                close_ind = sentence.rfind(close_sign_4)
                if(close_ind == -1):
                    close_ind = sentence.rfind(close_sign_5)
    return close_ind

def search_beginning(sentence):
    cur_sentence = sentence
    open_ind = wslash_open_sign_ind(cur_sentence) + 1
    close_ind = find_last_close_sign(cur_sentence)
    
    while open_ind < close_ind:
        cur_sentence = cur_sentence[:open_ind]
        open_ind = wslash_open_sign_ind(cur_sentence) + 1
        close_ind = find_last_close_sign(cur_sentence)
        
    cur_sentence = sentence[open_ind + 1:]
    return cur_sentence

def search_previous_sentences(open_signs_num, index, sentence_chunk, result_text):
    result_text.append(sentence_chunk)
    cur_result_ind = len(result_text) - 2
    while cur_result_ind > -1:
        
        open_signs_num = count_open_signs(result_text[cur_result_ind])
        close_signs_num = count_close_signs(result_text[cur_result_ind])
        
        if open_signs_num > close_signs_num:
            if open_signs_num == 1:
                    open_sign_ind = wslash_open_sign_ind(result_text[cur_result_ind]) + 1
                    result_text[cur_result_ind] = result_text[cur_result_ind][open_sign_ind:]
            else:
                new_sentence = search_beginning(result_text[cur_result_ind])
                result_text[cur_result_ind] = new_sentence
            break
        cur_result_ind = cur_result_ind - 1
    return result_text