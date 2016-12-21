from __future__ import print_function
import operator
import itertools
import collections
import math
import re
import json
#=======================================================================================

def indexer(tccorpus, index_file):
    
    tokens = []
    doc_tokens_list=[]
    doc_tokens = []
    doc_id = 1

    # Reading tccorpus.txt line by line
    with open(tccorpus) as f:
        lines = f.read().splitlines()
    #======================================================================================= 
    # creating doc_tokens_list
    # A list of dictionaries consisting of doc_id as keys
    # and tokens as values
    # structure :-
    # doc_tokens => dict{doc_id : tokens} 
    # doc_tokens_list => list[doc_tokens] 
    
    for line in lines:
        temp_token_list = line.split()
        if temp_token_list[0] == '#':
            doc_tokens_list.append(doc_tokens)
            doc_tokens = []
            continue
        else:
            for w in temp_token_list:
                if w.isdigit():
                    continue
                else:
                    if tokens is None:
                        tokens = [w]
                    else:
                       tokens.append(w)

                    if doc_tokens is None:
                        doc_tokens = [w]
                    else:
                        doc_tokens.append(w)
                       
    doc_tokens_list.append(doc_tokens)

    # total no. of tokens in doc set
    # length of doc set
    total_tokens = len(tokens)

    # fetching unique tokens to compute inverted index
    tokens = list(set(tokens))    

    #=============================================================================================
    # computing inverted index list
    # structure for inverted_index => dictionary of dictionaries
    # inverted_index => {'Token' : {doc_id : token_count}}
    print("computing inverted index list \n")
    inverted_index = dict((token, {}) for token in tokens)    

    doc_id = 0    
    i=1
        
    for token in tokens:
        print(i)
        i+=1
        temp_dict = {}
        doc_id = 0
        for doc_tokens in doc_tokens_list:
            count=0
            for w in doc_tokens:
                if w == token:
                    count += 1
        
            if count == 0:
                pass
            else:
                temp_dict[doc_id] = count                            
            doc_id += 1

        inverted_index[token] = temp_dict        

    print("completed computation for inverted index \n")
    print("converting inverted_index to json object file")
    with open(index_file, 'w') as fp:
        json.dump(inverted_index, fp)

    print("json parsing in progress")
    print("inverted_index.json file has been created")

#=======================================================================================

indexer('tccorpus.txt', 'index.out.json')   

