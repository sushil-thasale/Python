from __future__ import print_function
import operator
import itertools
import collections
import math

#=============================================================================================

pages = []
old_pr = {}
new_pr = {}

# reading graph as lines
with open('wt2g_inlinks.txt') as f:
    links = f.read().splitlines()
    
#converting to list of lists
graph = list(map(lambda s: s.split(), links))

print(len(graph))

#=============================================================================================
# All pages from graph
print("fetching pages from graph")
for row in graph:
    pages.append(row[0])

print(len(pages))

#=============================================================================================
# initial page rank
initial_pr = 1.0/len(pages)

print("calculating initial page rank")
for page in pages:
    old_pr[page]= initial_pr
  
#=============================================================================================
#inlinks - set of links pointing to p
print("entering inlink calc")

inlinks={}
inlink_counts={}

for row in graph:
    inlinks[row[0]] = list(set(row[1:len(row)]))

#=============================================================================================
# computing inlink count of each page 

for page in pages:
    inlink_counts[page] = len(inlinks.get(page))

# fetching nodes with no inlinks
nodes_with_no_inlinks=[]

for page in pages:
    if inlink_counts.get(page) == 0:
        nodes_with_no_inlinks.append(page)

print(len(nodes_with_no_inlinks))

#=============================================================================================
#proportion of pages with no inlinks
proportion_no_inlinks = 1.0*len(nodes_with_no_inlinks)/len(pages)
print("proportion of pages with no inlinks: ",proportion_no_inlinks)

#=============================================================================================
# top 50 pages with inlink counts
sorted_inlink_count=sorted(inlink_counts.items(), key=operator.itemgetter(1), reverse=True)
sorted_inlink_count2 = collections.OrderedDict(sorted_inlink_count)
top_50_inlinks = itertools.islice(sorted_inlink_count2.items(), 0, 50) # will return 1-50
 
#=============================================================================================
# fetching non-sink nodes
non_sink_nodes=[]

sorted_keys = sorted(inlinks.keys())
i=1
for key in sorted_keys:    
    print("key:", i)
    i+=1
    for inlink in inlinks.get(key):
        non_sink_nodes.append(inlink)        

non_sink_nodes = list(set(non_sink_nodes))

#=============================================================================================
#sink nodes - having no outlinks
sink_nodes=[]
print("fetching sink nodes")

#page in pages
#check if not present in non-sink
i=0
for page in pages:
    print(i)
    i+=1
    if page not in non_sink_nodes:
        sink_nodes.append(page)
    
sink_nodes = list(set(sink_nodes))
print("found sink nodes")

#=============================================================================================
# proportion of sink nodes to files

proportion_sink_nodes = 1.0*len(sink_nodes)/len(pages)
print("proportion of pages with no outlinks (sink nodes) : ", proportion_sink_nodes)
print(len(sink_nodes))
    
#=============================================================================================
#outlinks - set of pages pointed by p

outlinks={}
sorted_keys = sorted(inlinks.keys())
i=1

for key in sorted_keys:
    print("key:", i)
    i+=1
    for page in inlinks.get(key):
        if outlinks.get(page) is None:
            outlinks[page] = 1
            
        else:
            outlinks[page] = outlinks.get(page) + 1


#=============================================================================================
# top 50 pages with outlink counts
sorted_outlinks=sorted(outlinks.items(), key=operator.itemgetter(1), reverse=True)
sorted_outlinks2 = collections.OrderedDict(sorted_outlinks)
top_50_outlinks = itertools.islice(sorted_outlinks2.items(), 0, 50) # will return 1-50


#=============================================================================================
#computing page rank
    
d=0.85
perplexity={}
p_index = 0
p_index_temp2 =0
p_satisfy = 0
iteration_for_convergence = 0
perplexity_iteration_count=0    

while p_satisfy != 4:    
    for i in range(0,5):
        sink_pr=0
        for page in sink_nodes:
            sink_pr=sink_pr + old_pr[page]
            
        for page in pages:
            new_pr[page]=(1.0 - d)/len(pages) + d*sink_pr/len(pages)
            for inlink in inlinks[page]:
                new_pr[page] = new_pr[page] + d*old_pr[inlink]/int(outlinks.get(inlink))
                
        old_pr = new_pr

        #computing shannon enthropy
        shannon_enthropy = 0
        for page in pages:
            shannon_enthropy = shannon_enthropy + new_pr[page] * math.log(new_pr[page],2)

        #computing perplexity    
        perplexity[p_index] = math.pow(2,- shannon_enthropy)        
        p_index += 1       

    #checking for 4 consecutive iterations
    p_satisfy=0
    p_index_temp = p_index_temp2
    for i in range(0,4):
        print(perplexity.get(p_index_temp))
        if abs(perplexity.get(p_index_temp+1) - perplexity.get(p_index_temp)) < 1:            
            p_satisfy += 1            
        p_index_temp += 1

    p_index_temp2 += 1
    print("p_satisfy : ",p_satisfy)
    perplexity_iteration_count += 1
    print("iteration count : ",perplexity_iteration_count)

#=============================================================================================
iteration_for_convergence = perplexity_iteration_count
perplexity_computed_until_convergence = perplexity_iteration_count + 4
print("Page Rank have converged at : ", iteration_for_convergence)

sorted_perplexity = sorted(perplexity.items(), key=operator.itemgetter(0))
sorted_perplexity2 = collections.OrderedDict(sorted_perplexity)
perplexity_list_until_convergence = itertools.islice(sorted_perplexity2.items(), 0, perplexity_computed_until_convergence)
    
#=============================================================================================
# top 50 pages with highest pagerank
sorted_new_pr=sorted(new_pr.items(), key=operator.itemgetter(1), reverse=True)
sorted_new_pr2 = collections.OrderedDict(sorted_new_pr)
top_50_pr = itertools.islice(sorted_new_pr2.items(), 0, 50) # will return 1-50

#=============================================================================================
#pages with page rank less than their initial value
    
pages_with_less_pr = []
initial_pr = 1.0/len(pages)

for page in pages:
    if new_pr[page] < initial_pr:
        pages_with_less_pr.append(page)

proportion_pages_with_less_pr = len(pages_with_less_pr)/len(pages)                

#=============================================================================================
# writing to files        
#=============================================================================================
# writing inilinks and inlink_counts to files
with open('all_pages.txt', 'w') as f:
        f.write('\n'.join(pages))
        f.close()    

#=============================================================================================
with open('nodes_with_no_inlinks.txt', 'w') as f:
        f.write('\n'.join(nodes_with_no_inlinks))
        f.close()

#=============================================================================================
with open('top_50_inlinks.txt', 'w') as f:
    for t in top_50_inlinks:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()
    
#=============================================================================================
with open('perplexity_list_until_convergence.txt', 'w') as f:
    for t in perplexity_list_until_convergence:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()
#=============================================================================================
with open('sink_nodes.txt', 'w') as f:
        f.write('\n'.join(sink_nodes))
        f.close()

#=============================================================================================
with open ('outlinks.txt', 'w') as fp:
    for p in outlinks.items():
        fp.write("%s : %s\n" % p)  

#=============================================================================================
with open('top_50_outlinks.txt', 'w') as f:
    for t in top_50_outlinks:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()        

#=============================================================================================
with open('top_50_pr.txt', 'w') as f:
    for t in top_50_pr:
        f.write(' '.join(str(s) for s in t) + '\n')
    f.close()

#=============================================================================================
with open('pages_with_less_pr.txt', 'w') as f:
        f.write('\n'.join(pages_with_less_pr))
        f.close()

#=============================================================================================
with open ('new_pr.txt', 'w') as fp:
    for p in new_pr.items():
        fp.write("%s : %s\n" % p)         
        
#=============================================================================================                
with open('Page_Rank_Analysis.txt', 'w') as f:
        f.write("No. of Sink Nodes : ")
        f.write(str(len(sink_nodes)))
        f.write("\n")
        f.write("Proportion of Sink Nodes : ")
        f.write(str(proportion_sink_nodes))
        f.write("\n")
        f.write("Nodes with no inlinks : ")
        f.write(str(len(nodes_with_no_inlinks)))
        f.write("\n")
        f.write("Proportion of pages with no inlinks : ")
        f.write(str(proportion_no_inlinks))
        f.write("\n")
        f.write("No. of pages with page rank less than initial Page rank : ")
        f.write(str(len(pages_with_less_pr)))
        f.write("\n")
        f.write("Proportion of pages with page rank less than initial page rank : ")
        f.write(str(proportion_pages_with_less_pr))
        f.close() 

