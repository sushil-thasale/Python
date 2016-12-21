import os
import json
import math


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

    pos_word_count = {}
    i = 0
    for filename in os.listdir(os.getcwd()+ training_directory + "\\pos\\"):    
        print(i)
        i+=1
        with open(os.getcwd()+ training_directory + "\\pos\\" + filename) as f:
            lines = f.read().splitlines()
            for line in lines:
                temp_token_list = line.split()
                    
                for w in temp_token_list:
                    if w in filtered_tokens:
                        if pos_word_count.get(w) is None:
                            pos_word_count[w] = 1
                        else:
                            pos_word_count[w] = pos_word_count.get(w) + 1                                     
                 
        f.close()

    print(pos_word_count['the'])

    neg_word_count = {}
    i = 0
    for filename in os.listdir(os.getcwd()+ training_directory + "\\neg\\"):    
        print(i)
        i+=1
        with open(os.getcwd()+ training_directory + "\\neg\\" + filename) as f:
            lines = f.read().splitlines()
            for line in lines:
                temp_token_list = line.split()
                    
                for w in temp_token_list:
                    if w in filtered_tokens:
                        if neg_word_count.get(w) is None:
                            neg_word_count[w] = 1
                        else:
                            neg_word_count[w] = neg_word_count.get(w) + 1 
                 
        f.close()

    print(neg_word_count['the'])                
    #=====================================================================================================
        
    total_tokens_in_pos = 0
    for token in pos_word_count.keys():
        total_tokens_in_pos += pos_word_count.get(token)

    total_tokens_in_neg = 0
    for token in neg_word_count.keys():
        total_tokens_in_neg += neg_word_count.get(token)    

    print(total_tokens_in_pos)
    print(total_tokens_in_neg)
    #=====================================================================================================

    classes = ['pos','neg']
    mew = 1000
    cfw = 0
    big_c = total_tokens_in_pos + total_tokens_in_neg
    p_of_words_training = dict((class1, {}) for class1 in classes)

    for token in filtered_tokens:
        if pos_word_count.get(token) is None:
            pp = 0
        else:
            pp = pos_word_count.get(token)

        if neg_word_count.get(token) is None:
            pn = 0
        else:
            pn = neg_word_count.get(token)

        cfw = pp + pn
            
        #p_of_words_training['pos'][token] = 1.0*(pp + 1)/(total_tokens_in_pos + vocablary_size)
        #p_of_words_training['neg'][token] = 1.0*(pn + 1)/(total_tokens_in_neg + vocablary_size)

        p_of_words_training['pos'][token] = math.log(1.0*(pp + 1.0*mew*cfw/big_c)/(total_tokens_in_pos + mew))
        p_of_words_training['neg'][token] = math.log(1.0*(pn + 1.0*mew*cfw/big_c)/(total_tokens_in_neg + mew))


    with open('p_of_words_training_dirichlet.json', 'w') as fp:
            json.dump(p_of_words_training, fp)

    with open('filtered_tokens.json', 'w') as fp:
            json.dump(filtered_tokens, fp)        




#=====================================================================================================

nbtrain("\\textcat\\textcat\\train")


        
