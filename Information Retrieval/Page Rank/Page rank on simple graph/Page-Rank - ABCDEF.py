from __future__ import print_function

with open('graph_inlinks.txt') as f:
    links = f.read().splitlines()    

#converting to list of lists
graph = list(map(lambda s: s.split(), links))
print(graph)
#list(map(lambda x: print(x), graph))

#list of pages
pages = []
old_pr = {}
new_pr = {}
################################################
for row in graph:
    pages.append(row[0])

print(pages)
################################################
# initial page rank
for page in pages:
    old_pr[page]= 1.0/len(pages)
################################################
#sink nodes - having no outlinks
sink_nodes=[]

#non-sink nodes
non_sink_nodes=[]

for row in graph:
    for page in row[1:len(row)]:
        non_sink_nodes.append(page)

non_sink_nodes = list(set(non_sink_nodes))        

#page in pages
#check if present in non-sink        
for page in pages:
    if page not in non_sink_nodes:
        sink_nodes.append(page)
    
print(sink_nodes)

################################################
#inlinks - set of links pointing to p

inlinks={}

for row in graph:
    inlinks[row[0]] = list(set(row[1:len(row)]))

print(inlinks)
####################################################
#outlinks - set of pages pointed by p

outlinks={}

for page in pages:
    for row in graph:
        if not row[1:len(row)]:
            pass
        else:
            if page in row[1:len(row)]:
                if outlinks.get(page) is None:
                    outlinks[page] = row[0]
                else:
                    outlinks[page] = outlinks.get(page) + row[0]


print(outlinks)
####################################################
d=0.85



    
for i in range(0,100):
    sink_pr=0
    for page in sink_nodes:
        sink_pr=sink_pr + old_pr[page]
    for page in pages:
        new_pr[page]=(1.0 - d)/len(pages) + d*sink_pr/len(pages)
        for inlink in inlinks[page]:
                new_pr[page] = new_pr[page] + d*old_pr[inlink]/len(outlinks[inlink])
    old_pr = new_pr
    
print(new_pr)

with open ('pr_graph_100_iteration.txt', 'w') as fp:
    for p in new_pr.items():
        fp.write("%s : %s\n" % p)  













