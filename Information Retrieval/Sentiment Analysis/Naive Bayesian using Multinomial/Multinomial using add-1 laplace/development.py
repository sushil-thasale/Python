import collections
import math
import re
import json
import os
import operator
import itertools
import collections

def nbtest (test_directory, filtered_tokens, p_of_words_training, p_of_pos_neg):

    with open(p_of_words_training, 'r') as fp:
       p_of_words_training = json.load(fp)
   

    with open(filtered_tokens, 'r') as fp:
       filtered_tokens = json.load(fp)
       
    print(len(filtered_tokens))

    p_of_pos = 0.5
    p_of_neg = 0.5

    #=====================================================================================================

    doc_list = []
    given_class = {}
    pos_doc_count = 0
    for filename in os.listdir(os.getcwd()+ test_directory + "\\pos\\"):    
        pos_doc_count += 1
        if doc_list is None:
            doc_list = [filename]
        else:
            doc_list.append(filename)
        given_class[filename] = 'pos'

    print(len(doc_list))

    neg_doc_count = 0
    for filename in os.listdir(os.getcwd()+ test_directory + "\\neg\\"):    
        neg_doc_count += 1
        doc_list.append(filename)
        given_class[filename] = 'neg'

    print(len(doc_list))

    #=====================================================================================================

    inverted_doc = dict((doc_id, {}) for doc_id in doc_list)

    i=0
    for filename in os.listdir(os.getcwd()+ test_directory + "\\pos\\"):    
        print(i)
        i+=1
        with open(os.getcwd()+ test_directory + "\\pos\\" + filename) as f:
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

    for filename in os.listdir(os.getcwd()+ test_directory + "\\neg\\"):    
        print(i)
        i+=1
        with open(os.getcwd()+ test_directory + "\\neg\\" + filename) as f:
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

    print(inverted_doc['1576.txt']['okay'])
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

    print(p_of_c_given_d['pos']['1576.txt'])
    print(p_of_c_given_d['neg']['1576.txt'])

    #=====================================================================================================

    estimated_class = {}
            
    for doc_id in inverted_doc.keys():

        if p_of_c_given_d['pos'][doc_id] >= p_of_c_given_d['neg'][doc_id]:
            estimated_class[doc_id] = 'pos'
        else:
            estimated_class[doc_id] = 'neg'
        

    print(estimated_class['1576.txt'])
    print(estimated_class['1576.txt'])

    #=====================================================================================================

    with open('dev_results.txt', 'w') as f:
        for doc_id in estimated_class.keys():            
            f.write(doc_id + "\t" + "|" + "\t" + str(p_of_c_given_d['pos'][doc_id])
                    + "\t" + "|" + "\t" + str(p_of_c_given_d['neg'][doc_id])
                    + "\t" + "|" + "\t" + given_class.get(doc_id)
                    + "\t" + "|" + "\t" + estimated_class.get(doc_id) + '\n')        
    f.close()    

    #=====================================================================================================
    overall_correct_count = 0
    pos_correct_count = 0
    neg_correct_count = 0

    for doc_id in estimated_class.keys():    
        if estimated_class[doc_id] == given_class[doc_id]:
            overall_correct_count += 1

        if given_class[doc_id] == 'pos':
            if estimated_class[doc_id] == 'pos':
                pos_correct_count += 1

        if given_class[doc_id] == 'neg':
            if estimated_class[doc_id] == 'neg':
                neg_correct_count += 1            


    overall_percent_correct = 100.0*overall_correct_count/len(doc_list)
    pos_percent_correct = 100.0*pos_correct_count/pos_doc_count
    neg_percent_correct = 100.0*neg_correct_count/neg_doc_count

    with open('percent_correct.txt' , 'w') as f:
        f.write("overall correctness percent -> " + str(overall_percent_correct) + "\n")
        f.write("percent pos docs classified correctly -> " + str(pos_percent_correct) + "\n")
        f.write("percent neg docs classified correctly -> " + str(neg_percent_correct) + "\n")
    f.close()
        
#=====================================================================================================
    # computing log ratio - pos/neg
    # computing log ratio - neg/pos
    pos_to_neg_ratio = {}
    neg_to_pos_ratio = {}
    p = 0
    n = 0
    for w in filtered_tokens:
        p = p_of_words_training['pos'][w]

        n = p_of_words_training['neg'][w]

        if p == 0 or n == 0:
            pos_to_neg_ratio[w] = 0
        else:
            pos_to_neg_ratio[w] = p_of_words_training['pos'][w] / p_of_words_training['neg'][w]

        if n == 0 or p == 0:
            neg_to_pos_ratio[w] = 0
        else:
            neg_to_pos_ratio[w] = p_of_words_training['neg'][w] / p_of_words_training['pos'][w]

    sorted_pos_to_neg_ratio = sorted(pos_to_neg_ratio.items(), key=operator.itemgetter(1), reverse=True)    
    sorted_pos_to_neg_ratio2 = collections.OrderedDict(sorted_pos_to_neg_ratio)
    top_20_words_pos_to_neg = itertools.islice(sorted_pos_to_neg_ratio2.items(), 0, 20)

    sorted_neg_to_pos_ratio = sorted(neg_to_pos_ratio.items(), key=operator.itemgetter(1), reverse=True)    
    sorted_neg_to_pos_ratio2 = collections.OrderedDict(sorted_neg_to_pos_ratio)
    top_20_words_neg_to_pos = itertools.islice(sorted_neg_to_pos_ratio2.items(), 0, 20)

    with open('top_20_words_pos_to_neg.txt', 'w') as f:    
        for key,value in top_20_words_pos_to_neg:            
            f.write(str(key))            
            f.write("\t|\t")
            f.write(str(value))
            f.write("\n") 
    f.close()

    with open('top_20_words_neg_to_pos.txt', 'w') as f:    
        for key,value in top_20_words_neg_to_pos:            
            f.write(str(key))            
            f.write("\t|\t")
            f.write(str(value))
            f.write("\n")
    f.close()       
#=====================================================================================================
nbtest ("\\textcat\\textcat\\dev" , "filtered_tokens.json" , "p_of_words_training.json" , "p_of_pos_neg.txt")

## model file consist of three different files
## "filtered_tokens.json"
## "p_of_words_training.json"
## "p_of_pos_neg.txt"

        








