import collections
import math
import re
import json
import os

def nbtest (test_directory, filtered_tokens, p_of_words_training, p_of_pos_neg):

    with open(p_of_words_training, 'r') as fp:
       p_of_words_training = json.load(fp)


    with open(filtered_tokens, 'r') as fp:
       filtered_tokens = json.load(fp)
       

    p_of_pos = 0.5
    p_of_neg = 0.5

    #=====================================================================================================

    doc_list = []
    for filename in os.listdir(os.getcwd()+ test_directory + "\\"):

        if doc_list is None:
            doc_list = [filename]
        else:
            doc_list.append(filename)    

    print(len(doc_list))

    #=====================================================================================================

    inverted_doc = dict((doc_id, {}) for doc_id in doc_list)

    i=0
    for filename in os.listdir(os.getcwd()+ test_directory + "\\"):
        print(i)
        i+=1
        with open(os.getcwd()+ test_directory + "\\" + filename) as f:
            lines = f.read().splitlines()
            for line in lines:
                temp_token_list = line.split()
                    
                for w in temp_token_list:
                    if w in filtered_tokens:
                        if inverted_doc[filename].get(w) is None:
                            inverted_doc[filename][w] = 1
                        else:
                            inverted_doc[filename][w] = inverted_doc[filename].get(w) + 1
                 
        f.close()

    print(len(inverted_doc.keys()))
          
    #=====================================================================================================

    classes = ['pos','neg']

    p_of_c_given_d = dict((class1, {}) for class1 in classes)

    i=0
    for doc_id in inverted_doc.keys():
        print(i)
        i += 1
        log_sum_pos = 0.0
        log_sum_neg = 0.0
                
        
        for w in inverted_doc.get(doc_id).keys():
            
            if w in filtered_tokens:
                xp = p_of_words_training['pos'].get(w)
                xn = p_of_words_training['neg'].get(w)  
                            
                log_sum_pos += xp 
                log_sum_neg += xn                    

        p_of_c_given_d['pos'][doc_id] = log_sum_pos + math.log(p_of_pos)
        p_of_c_given_d['neg'][doc_id] = log_sum_neg + math.log(p_of_neg)


    #=====================================================================================================

    estimated_class = {}
            
    for doc_id in inverted_doc.keys():

        if p_of_c_given_d['pos'][doc_id] >= p_of_c_given_d['neg'][doc_id]:
            estimated_class[doc_id] = 'pos'
        else:
            estimated_class[doc_id] = 'neg'
        

    #=====================================================================================================

    with open('test_results.txt', 'w') as f:
        for doc_id in estimated_class.keys():            
            f.write(doc_id + "\t" + "|" + "\t" + str(p_of_c_given_d['pos'][doc_id])
                    + "\t" + "|" + "\t" + str(p_of_c_given_d['neg'][doc_id])                
                    + "\t" + "|" + "\t" + estimated_class.get(doc_id) + '\n')        
    f.close()    

    #=====================================================================================================


nbtest ("\\textcat\\textcat\\test" , "filtered_tokens.json" , "p_of_words_training.json" , "p_of_pos_neg.txt")



