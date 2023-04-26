import networkx as nx
import matplotlib.pyplot as p
import numpy as n
import math as m
import csv

#quality measures
def unifiability (G, Ci, Cj):
    sum1, sum2, sum3 = 0, 0, 0
    for i in Ci:
        for j in Cj:
            sum1 += 1 if G.has_edge(i, j) else 0
    for i in Ci:
        for j in G:
            sum2 += 1 if G.has_edge(i, j) else 0
        for j in Cj:
            sum2 -= 1 if G.has_edge(i, j) else 0
    for i in Cj:
        for j in G:
            sum3 += 1 if G.has_edge(i, j) else 0
        for j in Ci:
            sum3 -= 1 if G.has_edge(i, j) else 0
    return sum1 / (sum2 + sum3 - sum1)
#Average Uniformality
def AVU (G, cluster):
    #CALLING UNIFIABILITY FOR ALL CLUSTERS
    sum_unifiability = 0
    for i in cluster:
        for j in cluster:
            if i != j:
                sum_unifiability += unifiability (G, cluster[i], cluster[j])
    return sum_unifiability / len (cluster)

#Isolability
def isolability (G, Ci):
    sum1, sum2 = 0, 0
    for i in Ci:
        for j in Ci:
            sum1 += 1 if G.has_edge(i, j) else 0
    for i in Ci:
        for j in G:
            if i != j:
                sum2 += 1 if G.has_edge(i, j) else 0
    return sum1 / (sum1 + sum2)

#average isolabiltiy
def AVI (G, cluster):
    sum = 0
    for i in cluster:
        sum += isolability (G, cluster[i])
    return sum / len (cluster)

########################################
def print_matrix(A) :
    for row in A :
        print(row)
########################################
def adj_matrix(g) :
    n = g.number_of_nodes()
    #E=g.edges() 
    A=[ [0]*n for i in range(n)]
    #print_matrix(A)
    for (x, y) in g.edges():
        #print(x, ",", y)
        A[x][y]=A[y][x]=A[x][x]=A[y][y]=1
    return A
########################################
def sortByWeight(W, E) :
    sortWlist=sorted(W.items(), key=lambda x:x[1], reverse=True)
    E=list()
    W=dict()
    W=dict(sortWlist)
    for (key, val)  in sortWlist:
        E.append(key)
    return E, W
########################################
def merge(C):
    k=len(C)
    go=True
    for i in range(1, k):
        if(i<len(C) and go) :
            j = i - 1
            while j >= 0:
                if len(C[i].intersection(C[j])) >= len(C[i])/2 or  ( len(C[i])==2 and len(C[i].intersection(C[j]))>=1 ) :
                    C[j].union(C[i])
                    C.remove(C[i])
                    C = sorted(C, key=len, reverse=True)
                    go=False
                    break
                else :
                    j -= 1
        else :
            break
    return C
########################################
def printC(C) :
    i=0
    for c in C :
        print("C", i, " : ", c)
        i+=1
    print("\n")

#______________________$$ main $$______________________

'''g=nx.Graph()
g=nx.karate_club_graph()'''

g=nx.Graph()
with open("dolphins.csv", mode ='r') as file:
   csvFile = csv.DictReader(file)
   for line in csvFile:
        g.add_edge(int(line['Source'])-1, int(line['Target'])-1)

'''g=nx.Graph()
g.add_edge(0,1)
g.add_edge(0,3)
g.add_edge(1,2)
g.add_edge(1,4)
g.add_edge(2,3)
g.add_edge(2,5)
g.add_edge(3,4)
g.add_edge(4,5)
g.add_edge(5,6)
g.add_edge(5,10)
g.add_edge(6,7)
g.add_edge(6,9)
g.add_edge(6,10)
g.add_edge(7,8)
g.add_edge(8,9)
g.add_edge(10,11)
g.add_edge(10,12)
g.add_edge(11,12)'''

##_ GRAPH INFORMATION _##
V=g.nodes()
n=len(V)

E=list()
for (a, b) in g.edges() :
    if a<b :
        E.append((a, b))
    else :
        E.append((b, a))
#print("Edges : ", E)
        
deg = dict( g.degree() )
#print("Degree : ", deg)

A = adj_matrix(g)
#print_matrix(A)

N=dict()
for i in range(n) :
    Ni={i}
    for j in range(n) :
        if(A[i][j] == 1) :
            Ni.add(j)
    N[i]=Ni
#print("N = ", N, "\n")
########################################

W =dict()
for (i, j) in E :
    nij=0
    for k in range(n) :
        nij += A[i][k]*A[j][k]
    W[ (i,j) ] = nij / m.sqrt( (deg[i]+1) * (deg[j]+1) )

E, W=sortByWeight(W, E)
#print("E = ", E, "\nW = ")
#for key in W :
#    print(key, " : ", W[key])
    
C=[] # single vertex's community
for v in V :
    C.append({v})
#print("C=", C)

for (u, v) in E :
    #print("(", u, ", ", v, ")__________________________")
    s3=False #common_set_uv
    for c in C :
        if( (u in c) and (v in c) ) :
            s3=True
    
    if( ({u} in C) & ({v} in C) ) :
        C.remove({u})
        C.remove({v})
        C.append({u, v})

    elif( s3==False ) :
        #print("N[u] = ", N[u], ", N[v] = ", N[v])
        CNuv=0
        Cv_max=set()
        CNvu=0
        Cu_max=set()

        for com in C :
            if v in com : # Cv - must contain v
                a=com.intersection(N[u])
                if(len(a) > CNuv) :
                    CNuv=len(a)
                    Cv_max=com
                elif(len(a) == CNuv) :
                    if(len(Cv_max) < len(com)):
                        Cv_max=com
                        
            if u in com : # Cu - must contain u
                q=com.intersection(N[v])
                if(len(q) > CNvu) :
                    CNvu=len(q)
                    Cu_max=com
                elif(len(q) == CNvu) :
                    if(len(Cu_max) < len(com)):
                        Cu_max=com
               
        if CNuv > CNvu or ( CNuv == CNvu and deg[u] < deg[v] ) : # deg[u] < deg[v]  or deg[u] <= deg[v] 
            C.remove(Cv_max)
            Cv_max.add(u)
            C.append(Cv_max)
            if({u} in C) :
                    C.remove({u})
        else :
            C.remove(Cu_max)
            Cu_max.add(v)
            C.append(Cu_max)
            if({v} in C) :
                    C.remove({v})
    #print("(", u, ", ", v, "),  C : ", C )
    #print("(", u, ", ", v, "), W=", sorted_W[(u, v)], " C : ", C )

#printC(C)
C = sorted(C, key=len, reverse=True)
print("sorted by size of sets, C = ")
printC(C)

s1=0
s2=len(C)
while(s1!=s2) :
    s1=s2
    C=merge(C)
    s2=len(C)
print("final list C : ")
printC(C)

Nc=len(C)
print("Number of communities = Nc =", Nc)

'''colors=[i for i in range(len(C))]
print("______________colors=", colors)
Node_comlist=[[] for node in V]
for i in range(len(C)) :
    for node in C[i] :
        Node_comlist[node].append(i)
print(Node_comlist)

pos = nx.spring_layout(g)

fig = p.figure(figsize=(10,10))

nx.draw_networkx_edges(g, node_size=50, pos=pos, alpha=0.3) # node_color=colors,
cmap=p.cm.viridis

for node in g.nodes():
    part_of = Node_comlist[node]
    w = p.pie([1]*len(part_of), center= pos[node], colors=[cmap(q/Nc) for q in part_of], radius=0.05)'''

print("Overlapping Modularity = ", overlapping_modularity(g, C))
nx.draw_networkx(g, with_labels=True, edgecolors="black", edge_color="magenta", width=1, node_size=300, node_color="yellow" )
p.title("Graph")
p.show()
