import os
import json
import math
import operator
import itertools
import collections    

#file_path = path.relpath("textcat/textcat/train/neg/")
#with open(file_path) as f:

# dict containing doc_id and all tokens belonging to that doc
# all_tokens_pos_docs = {}
# all_tokens contains all tokens from pos and neg files
#all_tokens = []
def nbtrain(training_directory):
        
    pos_doc_count = 0
    token_count = {}
    for filename in os.listdir(os.getcwd()+ training_directory + "\\pos\\"):    
        with open(os.getcwd()+ training_directory + "\\pos\\" + filename) as f:
            pos_doc_count += 1
            lines = f.read().splitlines()
            for line in lines:
                temp_token_list = line.split()
                    
                for w in temp_token_list:
                    if token_count.get(w) is None:
                        token_count[w]=1
                    else:
                        token_count[w] = token_count.get(w) + 1
                 
        f.close()

    print(pos_doc_count)

    neg_doc_count = 0
    for filename in os.listdir(os.getcwd()+ training_directory + "\\neg\\"):    
        with open(os.getcwd()+ training_directory + "\\neg\\" + filename) as f:
            neg_doc_count += 1
            lines = f.read().splitlines()
            for line in lines:
                temp_token_list = line.split()
                    
                for w in temp_token_list:
                    if token_count.get(w) is None:
                        token_count[w]=1
                    else:
                        token_count[w] = token_count.get(w) + 1
                 
        f.close()
    
    print(neg_doc_count)
    #=====================================================================================================

    total_doc_count = pos_doc_count + neg_doc_count
    p_of_pos = 1.0*pos_doc_count/total_doc_count
    p_of_neg = 1.0*neg_doc_count/total_doc_count

    with open('p_of_pos_neg.txt', 'w') as f:
        f.write(str(p_of_pos) + '\n')
        f.write(str(p_of_neg) + '\n')
    f.close()    

    #=====================================================================================================

    filtered_tokens = []
    for token in token_count.keys():
        if token_count.get(token) >= 5:
            filtered_tokens.append(token)

    token_count = []
    print(len(filtered_tokens))
    vocablary_size = len(filtered_tokens)

    #=====================================================================================================
    classes = ['pos','neg']

    i = 0
    doc_tokens_list = dict((class1, {}) for class1 in classes)

    for filename in os.listdir(os.getcwd()+ training_directory + "\\pos\\"):    
        print(i)
        i+=1
        doc_tokens = []
        with open(os.getcwd()+ training_directory + "\\pos\\" + filename) as f:
            lines = f.read().splitlines()
            for line in lines:
                temp_token_list = line.split()
                for w in temp_token_list:
                    if doc_tokens is None:
                        doc_tokens = [w]
                    else:
                        doc_tokens.append(w)
                        
                                
        f.close()
        doc_tokens_list['pos'][filename] = doc_tokens


    for filename in os.listdir(os.getcwd()+ training_directory + "\\neg\\"):    
        print(i)
        i+=1
        doc_tokens = []
        with open(os.getcwd()+ training_directory + "\\neg\\" + filename) as f:
            lines = f.read().splitlines()
            for line in lines:
                temp_token_list = line.split()
                for w in temp_token_list:
                    if doc_tokens is None:
                        doc_tokens = [w]
                    else:
                        doc_tokens.append(w)
                        
                                
        f.close()
        doc_tokens_list['neg'][filename] = doc_tokens

    #print(doc_tokens_list['neg']['0049.txt'])
    #=====================================================================================================
        
    dfwc = dict((class1, {}) for class1 in classes)

    i=0
    for token in filtered_tokens:
        print(i)
        i+=1
        doc_count = 0
        for doc_id in doc_tokens_list['pos'].keys():
            if token in doc_tokens_list['pos'].get(doc_id):
                doc_count += 1
        dfwc['pos'][token] = doc_count

        doc_count = 0
        for doc_id in doc_tokens_list['neg'].keys():
            if token in doc_tokens_list['neg'].get(doc_id):
                doc_count += 1
        dfwc['neg'][token] = doc_count
                                
    #=====================================================================================================

    p_of_words_training = dict((class1, {}) for class1 in classes)
    p_of_words_training_2 = dict((class1, {}) for class1 in classes)
    

    for token in filtered_tokens:
        if dfwc['pos'].get(token) is None:
            pp = 0
        else:
            pp = dfwc['pos'].get(token)

        if dfwc['neg'].get(token) is None:
            pn = 0
        else:
            pn = dfwc['neg'].get(token)
            
        p_of_words_training['pos'][token] = math.log(1.0*(pp + 1)/(pos_doc_count + 1))
        p_of_words_training['neg'][token] = math.log(1.0*(pn + 1)/(neg_doc_count + 1))

        p_of_words_training_2['pos'][token] = (1.0*(pp + 1)/(pos_doc_count + 1))
        p_of_words_training_2['neg'][token] = (1.0*(pn + 1)/(neg_doc_count + 1))

    print(p_of_words_training['pos']['the'])
    print(p_of_words_training['neg']['the'])

    with open('p_of_words_training.json', 'w') as fp:
            json.dump(p_of_words_training, fp)

    with open('filtered_tokens.json', 'w') as fp:
            json.dump(filtered_tokens, fp)        

#=====================================================================================================
            
    # computing log ratio - pos/neg
    # computing log ratio - neg/pos
    pos_to_neg_ratio = {}
    neg_to_pos_ratio = {}
    p = 0
    n = 0
    for w in filtered_tokens:
        p = p_of_words_training_2['pos'][w]

        n = p_of_words_training_2['neg'][w]

        if p == 0 or n == 0:
            pos_to_neg_ratio[w] = 0
        else:
            pos_to_neg_ratio[w] = math.log(p_of_words_training_2['pos'][w] / p_of_words_training_2['neg'][w])

        if n == 0 or p == 0:
            neg_to_pos_ratio[w] = 0
        else:
            neg_to_pos_ratio[w] = math.log(p_of_words_training_2['neg'][w] / p_of_words_training_2['pos'][w])

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

nbtrain("\\textcat\\textcat\\train")
