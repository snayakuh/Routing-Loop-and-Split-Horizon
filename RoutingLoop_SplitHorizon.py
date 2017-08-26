
# coding: utf-8

# For simulating the routing loop the graph.jpg has been taken as an example Graph.jpg All the modules and steps are presented with the figure AllSteps.png
# Suppose the link from B to C fails. Before A knows about this link failure, it shares it's routing table with B.
# In this table B realizes A has a path to C but could not know the same path goes through B itself. B updates it's table and set path to C and the nexthop as A.
# However, A has the path to C but nexthop as B. In this scenario both A and B pointing to each other for the destination C as a resultany packet from A to C or B to C falls in a routing loop.
# Split horizon technique is used to solve this routing loop.

# In[194]:
"""
PREPARED BY:SUKANTI NAYAK
SIMULATION OF ROUTING LOOP AND ITS PREVENTION BY SPLIT HORIZON
Build Routing TableGraph API:
iter(graph) gives all nodes
iter(graph[u]) gives neighbours of u
graph[u][v] gives weight of edge (u, v)
"""
from IPython.display import Image
Image(filename='GRAPH.JPG')


# In[152]:

metrics = {
'A': {'B': 5, 'D': 9},
'B': {'A': 5, 'C': 3},
'C': {'B': 3,'D':2},
'D': {'A': 9,'C':2}
}


# In[153]:

#Build Routing Table using Routing Algorithm. Here Bellman ford Algorithm is used.
# Step 1: For each node prepare the destination and predecessor
def initialize(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for next hop
    for node in graph:
        d[node] = float('Inf') # initialisation to infinity
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p
#Step 2:Run the Routing algorithm
def Routing_Algo(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbour of u
                if d[v] > d[u] + graph[u][v]:
                # Record this lower distance
                    d[v] = d[u] + graph[u][v]
                    p[v] = u
# Step 3: check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            assert d[v] <= d[u] + graph[u][v]
    return d, p


# In[154]:

#Building Routing Table for each node
# Node A
def BuildRoutingTable(metrics,source):
    d, p=Routing_Algo(metrics, source)
    #print the cost and next hop
    m=3
    n=4
    RT=[[0] * m for i in range(n)]
    x=0
    for i,j,k in zip(d.keys(),d.values(),p.values()):
        y=0
        RT[x][y]=i
        y=y+1
        RT[x][y]=j
        y=y+1
        RT[x][y]=k
        x=x+1
    return RT


# In[192]:

#SENDING PACKETS FROM Node A TO NODE C
def sendpackets(s,d,sm,count):
    if (count>n):
        print("         ############################## ")
        print ("         # Routing Loop is discovered #")
        print("         # Unsuccessful Transmission  #")
        print("         ############################## ")
    else:
        print("-----------------------------")
        print("Look Up at ",s)
        print("-----------------------------")
        for i in range(0,4):
            nexthop=sm[i][2]
            if(nexthop=='A'):
                nexthopmatrix= A
            if(nexthop=='B'):
                nexthopmatrix= B
            if(nexthop=='C'):
                nexthopmatrix= C    
            if(nexthop=='D'):
                nexthopmatrix= D
            if (sm[i][0]==d):
                if(sm[i][1]==float('Inf')):
                    print("############################################")
                    print("# Destination Unreachable due to Link Fail #")
                    print("############################################")
                elif (nexthop==s):
                    print("Next hop is destination")
                    print("-----------------------------")
                    print("Reached Destination",d)
                    print("        ###########################  ")
                    print("        # Successful Transmission #  ")
                    print("        ###########################  ")
                else:
                    sendpackets(nexthop,d,nexthopmatrix,count+1)
                break  


# In[172]:

def BuildTableWithSharedInfo(n1,n2,RT1,RT2):
    print("-------------------------------")
    print("With Shared Info, Building New table at",n2)
    for i in range (0,4):
        if (RT2[i][0]==n1):
            CostToNeighour=RT2[i][1]
    for i in range (0,4):
        if (RT2[i][1] > CostToNeighour+RT1[i][1]):
            print("--------------------------")
            print("A New Update is Found for destination", RT2[i][0])
            RT2[i][1] = CostToNeighour+RT1[i][1]
            RT2[i][2]=n1
    return RT2


# In[157]:

#Link Failure and Updated Routing Table
def linkfail(node1,node2):
    #graph[node1][node2]=float('Inf')
    print("------------------------")
    print("B's Updated Table When Link Fails")
    print("--------------------------------------------")
    node1[1][1]=float('Inf')
    node1[1][2]=None
    print (node1)
    return node1


# In[158]:

def sharetable(A,B): 
    print("---------------------------------------------------------------")
    print ("A shares it's table without knowing about link fail")
    m=2
    n=4
    ShareData=[[0] * m for i in range(n)]
    for i in range (0,4):
        ShareData[i][0]=A[i][0]
        ShareData[i][1]=A[i][1]
    print("---------------------------------------------------------------")
    print ("A's shared  table is")  
    print(ShareData)
    print("---------------------------------------------------------------")
    print("B bulids new routing table with A's info")
    B=BuildTableWithSharedInfo('A','B',ShareData,B)
    print("---------------------------------------------------------------")
    print("A's Routing Table")
    print("---------------------------------------------------------------")
    print (A) 
    print("---------------------------------------------------------------")
    print("B's New Routing Table after Link Fail")
    print("---------------------------------------------------------------")
    print (B) 
    return B


# In[187]:

def splithorizon(S,D,A,B):
    m=2
    n=4
    ShareData=[[0] * m for i in range(n)]
    for i in range (0,4):
        if(A[i][2]==D):
            ShareData[i][0]=A[i][0]
            ShareData[i][1]=float('Inf')
        else:
            ShareData[i][0]=A[i][0]
            ShareData[i][1]=A[i][1]
    print("------------------------------------------------------------")
    print ("A's shared  table is")  
    print(ShareData)
    print("------------------------------------------------------------")
    print("B bulids new routing table with A's info")
    B=BuildTableWithSharedInfo('A','B',ShareData,B)
    print("------------------------------------------------------------")
    print("A's Routing Table")
    print("------------------------------------------------------------")
    print (A) 
    print("------------------------------------------------------------")
    print("B's New Routing Table after Link Fail")
        print("---------------------------------------------------------")
    print (B) 
    return B


# In[173]:
"""
PREPARED BY:SUKANTI NAYAK
Build Routing Table
Graph API:
iter(graph) gives all nodes
iter(graph[u]) gives neighbours of u
graph[u][v] gives weight of edge (u, v)
"""
#Simulation of Routing Loop 
import pdb
import numpy
A=BuildRoutingTable(metrics,'A')
B=BuildRoutingTable(metrics,'B')
C=BuildRoutingTable(metrics,'C')
D=BuildRoutingTable(metrics,'D')
def main(A,B,C,D):
    #All nodes build Routing table with intial metrics
    print("\n")
    print("\n*****************Building Routing Table****************\n")
    print ("----------------------------------------------------")
    print("A's Routing Table")
    print(A)
    print ("----------------------------------------------------")
    print("B's Routing Table")
    print(B)
    print ("----------------------------------------------------")
    print("C's Routing Table")
    print(C)
    print ("----------------------------------------------------")
    print("D's Routing Table")
    print(D)
    #Transmit Packets from A to C
    print("\n")
    print("\n*************Transmit Packets from A to C************\n")
    sendpackets('A','C',A,1) 
    #Link Fails from B to C
    print("\n")
    print("\n****************Link Fails from B to C*************\n")
    print("------------------------")
    B=linkfail(B,C)
    #A Shares its Table to B
    print("\n")
    print("\n************Shared Table Occurs Periodically ***********\n")
    print("------------------------")
    print("A shares Table with B")
    B=sharetable(A,B)
    # After Link Failure,Send Packets from A to C Using New Table
    print("\n")
    print("\n**********After Link Failure,Send Packets from A to C ********\n")
    print("------------------------")
    sendpackets('A','C',A,1)
main(A,B,C,D)


# In[193]:

#Simulation of Routing Loop and it's Solution as split Horizon
import pdb
import numpy
"""
PREPARED BY:SUKANTI NAYAK
Graph API:
iter(graph) gives all nodes
iter(graph[u]) gives neighbours of u
graph[u][v] gives weight of edge (u, v)
"""
A=BuildRoutingTable(metrics,'A')
B=BuildRoutingTable(metrics,'B')
C=BuildRoutingTable(metrics,'C')
D=BuildRoutingTable(metrics,'D')
def main(A,B,C,D):
    #All nodes build Routing table with intial metrics
    print("\n")
    print("\n*****************Building Routing Table****************\n")
    print ("-------------------------------------------------------")
    print("A's Routing Table")
    print(A)
    print ("-------------------------------------------------------")
    print("B's Routing Table")
    print(B)
    print ("-------------------------------------------------------")
    print("C's Routing Table")
    print(C)
    print ("-------------------------------------------------------")
    print("D's Routing Table")
    print(D)
    #Transmit Packets from A to C
    print("\n")
    print("\n*************Transmit Packets from A to C***********\n")
    sendpackets('A','C',A,1) 
    #Link Fails from B to C
    print("\n")
    print("\n****************Link Fails from B to C****************\n")
    print("------------------------")
    B=linkfail(B,C)
    #A Shares its Table to B
    print("\n")
    print("\n**********Shared Table Using Split Horizon **********\n")
    print("------------------------")
    print("A shares Table with B")
    B=splithorizon('A','B',A,B)
    # After Link Failure,Send Packets from A to C Using New Table
    print("\n")
    print("\n********After Link Failure,Send Packets from A to C ********\n")
    print("------------------------")
    sendpackets('A','C',A,1)
main(A,B,C,D)


# In[ ]:



