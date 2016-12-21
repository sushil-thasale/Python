import os
import json
import math

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

    mew = 1000
    N = pos_doc_count + neg_doc_count
    Nw = 0
    for token in filtered_tokens:
        if dfwc['pos'].get(token) is None:
            pp = 0
        else:
            pp = dfwc['pos'].get(token)

        if dfwc['neg'].get(token) is None:
            pn = 0
        else:
            pn = dfwc['neg'].get(token)

        Nw = pp + pn
        p_of_words_training['pos'][token] = math.log(1.0*(pp + 1.0*mew*Nw/N)/(pos_doc_count + mew))
        p_of_words_training['neg'][token] = math.log(1.0*(pn + 1.0*mew*Nw/N)/(neg_doc_count + mew))

    print(p_of_words_training['pos']['the'])
    print(p_of_words_training['neg']['the'])

    with open('p_of_words_training_Bernouli_dirichlet.json', 'w') as fp:
            json.dump(p_of_words_training, fp)

    with open('filtered_tokens.json', 'w') as fp:
            json.dump(filtered_tokens, fp)        

#=====================================================================================================

nbtrain("\\textcat\\textcat\\train")
