from __future__ import print_function
import operator
import itertools
import collections
import math
import re
import json

#=============================================================================================

def bm25(indexer, query_file, top_n):

    # converting JSON object to inverted_index dictionary
    with open(indexer, 'r') as fp:
        inverted_index = json.load(fp)

    #==================================================
    # computing length of doc set    
    doc_ids = []
    for token in inverted_index:
        doc_ids = doc_ids + list(inverted_index.get(token).keys())

    doc_ids = list(set(doc_ids))
    N = len(doc_ids)
    print("Number of documents in doc set : ",N)
    #==================================================

    # reading query file line by line
    with open(query_file) as q:
        query_lines = q.read().splitlines()

    query_id = 1
    query_dict = {}

    # creating dictionary for queries
    # query_dict => {query_id : query}
    
    for query in query_lines:
        query_dict[query_id] = query
        query_id += 1

    #==================================================
    query_terms = []
    query_terms_list = []

    # creating dictionary to store query term frequency
    # query_term_freq => {'query_id' : {'query_term' : count}}
    
    query_term_freq = dict((key, {}) for key in query_dict.keys())

    print("computing query term frequency \n")
    i=1
    for key in query_dict.keys():
        print(i)
        i+=1
        query_terms = query_dict.get(key).split()
        query_terms_list.append(query_terms)
        unique_query_terms = set(query_terms)
        term_freq = {}
        for unique_term in unique_query_terms:
            count = 0
            for term in query_terms:
                if unique_term == term:
                    count += 1
            term_freq[unique_term] = count
        query_term_freq[key] = term_freq    
    
    print("completed computation for query term freq")    

    #==================================================

    # no relevance information
    r=0
    R=0

    # defining constants
    k1 = 1.2
    b = 0.75
    k2 = 100

    #==================================================
        
    # computing total token in doc to calculate avdl
    total_doc_length = 0
    for token in inverted_index.keys():
        temp = inverted_index.get(token)
        for doc_id in temp.keys():
            total_doc_length = total_doc_length + int(temp.get(doc_id))
            
    avdl = 1.0*int(total_doc_length)/N
    print("avg doc length : ",avdl)

    #==================================================
    
    # creating dictionary to length of each doc
    # doc_len => {doc_id : doc_length}
    doc_len={}
    for doc_id in range(1,N+1):
        length = 0
        for token in inverted_index:
            doc_dict = inverted_index.get(token)
            temp = doc_dict.get(str(doc_id))
            if temp is None:
                pass
            else:
                length = length + int(temp)
        doc_len[doc_id]=length

    #==================================================
        
    # computing (dl/avdl) ratio for each doc
    # doc_dl_avdl_ratio => {doc_id : dl/avdl}
    doc_dl_avdl_ratio = {}        
    for doc_id in doc_len:
        doc_dl_avdl_ratio[doc_id] = 1.0*int(doc_len.get(doc_id))/avdl
        doc_id += 1

    #==================================================  
    unique_terms=[]

    for query in query_lines:
        term_list = query.split()
        unique_terms = unique_terms + term_list

    unique_terms = list(set(unique_terms))

    # computing document term frequeny
    # no. of documents in which given query term occurs (n)
    # document_term_freq => {query_term : n}    

    document_term_freq = {}

    for unique_term in unique_terms:            
        doc_count = len(inverted_index.get(unique_term).keys())
        document_term_freq[unique_term] = doc_count

    print("computation on for doc term freq is completed")    

    #==================================================
    # Implementing BM25 algo
    BM25 = {}    
    print("implementing BM25 algo")

    i=1
    for query_id in query_term_freq.keys():
        print(i)
        i+=1
        BM25_query_doc = {}
        for doc_id in range(1,N):
            BM25_temp = 0
            K = k1 * ((1 - b) + b*doc_dl_avdl_ratio[doc_id])
            for query_term in query_term_freq.get(query_id):
                n = document_term_freq[query_term]
                if n is None:
                    n=0
                
                temp_dict = query_term_freq.get(query_id)
                qf = temp_dict.get(query_term)
                if qf is None:
                    qf=0

                temp_dict = inverted_index.get(query_term)
                if temp_dict is None:
                    f = 0
                else:
                    f = temp_dict.get(str(doc_id))
                if f is None:
                    f=0    

                term1 = ((r + 0.5)/(R - r + 0.5))/((n - r + 0.5)/(N - n - R + r + 0.5))
                
                if term1 == 0:
                    log_value = 0
                else:
                    log_value = math.log(term1)
                    
                term2 = f*(k1 + 1)/(K + f)
                term3 = qf*(k2 + 1)/(k2 + qf)
                product = log_value * term2 * term3
                
                BM25_temp = BM25_temp + product

            if not BM25_temp == 0:
                BM25_query_doc[doc_id] = BM25_temp

        BM25[query_id] =  BM25_query_doc   
           
    print("Computation for BM25 has been completed")            

    #=============================================================================================
    # sorthing as per BM25 score and fetching top 100 docs of each query
    
    output_file = 'result.eval.txt' 
    with open(output_file, 'w') as f:
        for query_id in BM25.keys():
            bm25_temp = BM25.get(query_id)
            sorted_bm25_doc = sorted(bm25_temp.items(), key=operator.itemgetter(1), reverse=True)
            sorted_bm25_doc2 = collections.OrderedDict(sorted_bm25_doc)
            top_50_docs = itertools.islice(sorted_bm25_doc2.items(), 0, top_n)
            rank = 1
            for key,value in top_50_docs:
                f.write(str(query_id))
                f.write("\t|\t")
                f.write(query_dict[query_id])
                f.write("\t|\t")
                f.write(str(key))
                f.write("\t|\t")
                f.write(str(rank)) 
                f.write("\t|\t")
                f.write(str(value))
                f.write("\t|\t")
                f.write("Sushil_PC")
                f.write("\n")
                rank += 1
    f.close() 
        
    #=============================================================================================

bm25('index.out.json', 'queries.txt', 100)
