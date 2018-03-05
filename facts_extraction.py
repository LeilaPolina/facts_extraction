#!/usr/bin/python
import argumentsExtractor as argExtr
import predicateExtractor as predExtr
import os
import codecs
import json
news_path = os.path.dirname(os.path.abspath(__file__)) + '/malt_news_json/'
facts_path = os.path.dirname(os.path.abspath(__file__)) + '/news_facts/'
parsing_result_path=os.path.dirname(os.path.abspath(__file__)) + '/parsing-result/'

def process_parse_sentences(filename):
    processed_sentences= []
    sentence = []
    for line in codecs.open(filename, 'r', 'utf-8'):
        if len(line) == 1:
            processed_sentences.append(sentence)
            sentence=[]
        else:
            word = line.split("\t")
            if (word[7]!='PUNC'):
                t={'id':int(word[0]),'form':word[1], 'first_form':word[2],'pos':word[3],'morf':list(word[5]),'parent':int(word[6]),'deprel':word[7]}
                sentence.append(t)
    return processed_sentences

def write_facts(filename,facts):
    file=filename.split('-')
    news_json_filename=news_path+file[0]+'.json'
    facts_json_filename=facts_path+file[0]+'-facts'+'.json'
    data=json.load(codecs.open(news_json_filename, 'r', 'utf-8-sig'))
    fact_json={}
    fact_json['title']=data['title']
    fact_json['pubdDate']=data['pubDate']
    fact_json['facts']=facts
    with codecs.open(facts_json_filename, 'w', encoding='utf-8-sig') as f:
        json.dump(fact_json, f, ensure_ascii=False)

def get_facts():
	
	for filename in os.listdir(parsing_result_path):
		sentences=process_parse_sentences(parsing_result_path+filename)
		counter=1 
		roots=[]
    
		for sent in sentences:
			root=predExtr.get_root(sent) 
			if(len(root)!=0):
				roots.append([counter, root]) 
			counter=counter+1

		facts=[]
		for root in roots:
			sent_id=root[0]-1
			root_id=root[1][0][0]
			subject=argExtr.get_subject(sentences[sent_id],root_id)
			obj=argExtr.get_object(sentences[sent_id],root_id,subject)
			adposition=argExtr.get_adposition(sentences[sent_id],root[1])
			adp_args=[]
        
			if(adposition!=None): 
				adp_args=argExtr.get_adposition_args(sentences[sent_id],adposition)
			if(subject!=[]):
				fact={}
				if(adp_args!=None):
					if(len(adp_args)>1):
						fact={ 'Subject':argExtr.get_elem(sentences[sent_id], subject),
							   'Predicate':argExtr.get_elem(sentences[sent_id],predExtr.get_full_root(root)),
							   'Arg1':argExtr.get_elem(sentences[sent_id], obj),
                               'Arg2':argExtr.get_elem(sentences[sent_id], adp_args)}
                    
					else:
						fact={ 'Subject':argExtr.get_elem(sentences[sent_id], subject),
                           'Predicate':argExtr.get_elem(sentences[sent_id],predExtr.get_full_root(root)),
                           'Arg1':argExtr.get_elem(sentences[sent_id], obj),
						   'Arg2':""}
			facts.append(fact)
		write_facts(filename,facts)

if __name__ == "__main__":
	get_facts() 