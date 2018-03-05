#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import json

def is_valid_noun_arg(arg):
	if(arg['deprel']==u'аппоз' or arg['deprel']==u'компл-аппоз' or arg['deprel']==u'об-аппоз' or arg['deprel']==u'нум-аппоз'):
	    return True
        if(arg['deprel']==u'квазиагент' or arg['deprel']==u'количест' or arg['deprel']==u'предл' or arg['deprel']==u'электив'):
            return True
        elif (arg['deprel']==u'опред' and arg['pos']!='V'):
            return True
        elif(arg['first_form']!=u'-' and arg['pos']==u'-' and arg['morf']==u'-'):
            return True
        elif (arg['deprel']==u'1-компл'  or arg['deprel']==u'сравнит' or arg['deprel']==u'2-компл'):
            return True
        elif(arg['deprel']==u'атриб' and arg['pos']!='S'):
            return True
        else:
            return False

noun_args=[]
def get_noun_args(sentence,root):
    for s in sentence:
        if (s['parent']==root and is_valid_noun_arg(s)):
            noun_args.append(s['id'])
            get_noun_args(sentence, s['id'])

def get_conjunction (sentence,root):
    conj_id=None
    for s in sentence:
        if(s['parent']==root and s['deprel']==u'сочин'):
            conj_id=s['id']
            
    if(conj_id!=None):
        for s in sentence:
            if(s['parent']==conj_id and s['deprel']==u'соч-союзн'):
                conj_id=s['id']
                return conj_id
    return conj_id

def add_args(main_lst,args):
    for arg in args:   
        main_lst.append(arg)
    del args[:]

	
def get_subject(sentence, root):
    subject=[]
    predic_counter=0 #иногда парсер ошибается и помечает несколько аргументов с предикативной связью,
    for s in sentence: #поэтому пришлось завести счётчик, чтобы только один раз брал такой аргумент, в принципе субъект обычно в начале предложения бывает, так что работает нормально в большистве случаев 
        if(predic_counter==0 and s['parent']==root 
           #берутся субъекты-существительные, но бывает так, что попадается какое-нибудь слово, типа "яндекс" или "блокчейн",
           #тогда парсер заполняет только первую форму и указывает тип связи, а другие св-ва не заполняет, поэтому морфологию не выходит учитывать
		   and (s['pos']=='N' or (s['first_form']!=u'-' and s['pos']==u'-' and s['morf']==u'-'))
           and  (s['deprel']==u'предик' or s['deprel']==u'огранич')):
            subject.append(s['id'])
			#проверяется, есть ли сочинительная связь
            conj=get_conjunction(sentence,s['id'])
			#если есть, то будут браться сочинительные аргументы и затем добавляться в субъект
            if(conj!=None):
                subject.append(conj)
                get_noun_args(sentence,conj)
                if(len(noun_args)!=0):
                    add_args(subject,noun_args)   
            get_noun_args(sentence,s['id'])
			#берутся аргументы субъекта
            if(len(noun_args)!=0):
                add_args(subject,noun_args)
            predic_counter+=1
    return sorted(subject)

def get_elem(sentence,args):
    result=""
    for arg_id in args:
        for s in sentence:
            if(s['id']==arg_id):
                result=result+' '+s['form']
    return result


def get_adposition_args(sentence,root):
    adposition_args=[]
    adposition_args.append(root)
    for s in sentence: 
        if(s['parent']==root and s['pos']!='P' and
			(s['deprel']==u'предл' or s['deprel']==u'атриб' or s['deprel']==u'аппоз' or (s['deprel']==u'опред' and s['deprel']=='M'))):    
            adposition_args.append(s['id'])
            if(s['pos']=='N' or s['pos']=='M' or s['first_form']!=u'-' ):
                get_noun_args(sentence,s['id'])
                if(len(noun_args)!=0):
                    add_args(adposition_args,noun_args)            
            return sorted(adposition_args)

def get_pass_analit_predicate_part(root):
    pass_analit_id=None
    for r in root:
        if(r[1]==u'пасс-анал'or r[1]==u'присвяз'):
            pass_analit_id=r[0]
            return pass_analit_id
    return pass_analit_id

#функция для обстоятельства
def get_adposition(sentence,root):
    adposition=None
    if(len(root)==1):
        for s in sentence:
		    #берутся только обстоятельства места или времени
            if(s['parent']==root[0][0] and (s['deprel']==u'обст' or s['deprel']==u'присвяз') and ((s['pos']=='S' and s['morf'][3]=='l') or s['pos']=='M')):
                adposition=s['id']
    else:
        #иногда обстоятельство связано с пассивно-аналитической частью корня, поэтому если от самого корня не вышло что-то вытащить,
        #то проверяется, если пасс-анал. часть и от неё будет браться обстоятельство
        pass_analit_id=get_pass_analit_predicate_part(root)
        if(pass_analit_id!=None):
            for s in sentence:
                if(s['parent']==pass_analit_id and s['deprel']==u'обст' and ((s['pos']=='S' and s['morf'][3]=='l') or s['pos']=='M')):
                    adposition=s['id']    
    return adposition


def is_valid_compl_arg(arg,subj):
    if(arg['deprel']==u'1-компл' or arg['deprel']==u'агент'):
        return True
    elif ((arg['deprel']==u'2-компл' or arg['deprel']==u'3-компл') and (arg['pos']=='N' or arg['pos']=='S' or arg['pos']=='V')):
        return True
    else:
        return False

def get_object(sentence, root, subj):
    obj=[]
    for s in sentence: 
        if(s['parent']==root and is_valid_compl_arg(s,subj)):
                if(s['pos']=='S' or s['pos']=='N' or s['pos']=='V' or s['pos']=='M' or s['pos']==u'-'):
                    obj.append(s['id'])
                    get_noun_args(sentence,s['id'])
                    if(len(noun_args)!=0):
                        add_args(obj,noun_args)
    return sorted(obj)



               

