#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_pod_arg(root,sentence):
    pod=None
    pod_arg=None
    for s in sentence:
        if((s['deprel']==u'1-компл' or s['deprel']==u'предик') and s['pos']=='C' and s['form']==u'что'):
            pod=s['id']
    if(pod!=None):
        for s in sentence:
            if(s['parent']==pod and s['pos']=='V' and s['deprel']==u'подч-союзн'):
                pod_arg=(s['id'],s['deprel']) 
    return pod_arg

#на случай, когда выделился корень-союз
def get_conj_part(root,sentence):
    arg=None
    for s in sentence:
        if(s['parent']==root and s['pos']=='V' and s['deprel']==u'соч-союзн'):
            arg=(s['id'],s['deprel'])
    return arg

def get_root(sentence):
    root=None
    predicate_parts=[]
    root_counter=0
    
    for s in sentence:
        if(root_counter==0 and s['deprel']=="ROOT"):
            if(s['pos']=="V"):
                root=(s['id'],s['deprel']) 
                root_counter+=1
            if(s['pos']=='C'):
                root=get_conj_part(s['id'],sentence)
                
    pod_arg=get_pod_arg(root,sentence)
    if(pod_arg!=None):
        root=pod_arg
    
        
    if(root!=None):  
        predicate_parts.append(root)
        for s in sentence:
            if(s['parent']==root[0] and
					(((s['deprel']==u'аналит' or s['deprel']==u'пасс-анал')and s['form'].lower()!=u'бы') or
                    (s['deprel']==u'огранич' and s['pos']=='Q' and s['form'].lower()!=u'также' and s['form'].lower()!=u'тоже') or
                    (s['deprel']==u'присвяз' and s['pos']=='N'))):
                predicate_parts.append((s['id'],s['deprel'])) 
    return predicate_parts

def get_full_root(root):
    full_root=[]
    for r in root[1]:
        full_root.append(r[0])
    return sorted(full_root)