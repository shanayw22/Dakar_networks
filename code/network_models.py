import networkx as nx
import numpy as np
import random 

#---------------------
#RANDOM GRAPH
#---------------------
def gnp_random_graph(N,p,directed=False,output="graph"):

    if output=="snapshots": snapshots=[]

    #INITIALIZE GRAPH
    if directed: 
        G=nx.DiGraph()
    else:
        G=nx.Graph()
       
    #CREATE NODES
    G.add_nodes_from([*range(0,N)])

    #CREATE EDGES
    node_list_1=list(G.nodes)
    for i in range(0,len(G.nodes)):
        if directed:
            list2=[*range(0,len(G.nodes))]
        else:
            list2=[*range(i,len(G.nodes))]
        for j in list2:
            if(i!=j): 
                test=np.random.uniform(0,1)
                if(test<p):
                    #tmp=G.copy()
                    #print(len(tmp.nodes))
                    if output=="snapshots": snapshots.append(G.copy())
                    G.add_edge(node_list_1[i],node_list_1[j])

    #RETURN EITHER A NETWORK OR SEQUENCE OF NETWORKS
    out=G
    if output=="snapshots":
        out=snapshots
    if output=="graph":
        out=G

    return out

#---------------------
# NON-LINEAR PREFERENTIAL ATTACHMENT MODEL 
#---------------------
def nonlinear_preferential_attachment(N, m, p, directed=False, output="graph"):
    if output=="snapshots": snapshots=[]
    if directed: 
        G=nx.DiGraph()
    else:
        G=nx.Graph()
    G.add_nodes_from([*range(0,m)])

    for new_node in range(m, N):
        G.add_node(new_node)
        degrees = np.array([G.degree(n)**p for n in G.nodes() if n != new_node])
        existing_nodes = [n for n in G.nodes() if n != new_node]

        if degrees.sum() > 0:
            probs = degrees / degrees.sum()
            targets = np.random.choice(existing_nodes, size=m, replace=False, p=probs)
        else:
            targets = np.random.choice(existing_nodes, size=m, replace=False)

        for target in targets:
            G.add_edge(new_node, target)

        if output == "snapshots": snapshots.append(G.copy())
    out=G
    if output=="snapshots":
        out=snapshots
    if output=="graph":
        out=G

    return out


#--------------------- 
# ATTRACTIVENESS MODEL 
#---------------------
def attractiveness(N, m, a, directed=False, output="graph"):
    if output=="snapshots": snapshots=[]
    if directed: 
        G=nx.DiGraph()
    else:
        G=nx.Graph()
    G.add_nodes_from([*range(0,m)])

    for new_node in range(m, N):
        G.add_node(new_node)
        degrees = np.array([G.degree(n) + a for n in G.nodes() if n != new_node])
        existing_nodes = [n for n in G.nodes() if n != new_node]
        
        if degrees.sum() > 0:
            probs = degrees / degrees.sum()
            targets = np.random.choice(existing_nodes, size=m, replace=False, p=probs)
        else:
            targets = np.random.choice(existing_nodes, size=m, replace=False)

        for target in targets:
            G.add_edge(new_node, target)

        if output == "snapshots": snapshots.append(G.copy())
    out=G
    if output=="snapshots":
        out=snapshots
    if output=="graph":
        out=G

    return out

#---------------------
# FITNESS MODEL
#---------------------
def fitness(N, m, directed=False, output="graph"):
    if output=="snapshots": snapshots=[]
    if directed: 
        G=nx.DiGraph()
    else:
        G=nx.Graph()
    G.add_nodes_from([*range(0,m)])

    int_fit = np.random.uniform(0, 10, size=N)

    for new_node in range(m, N):
        G.add_node(new_node)
        degrees = np.array([G.degree(n) * int_fit[n] for n in G.nodes() if n != new_node])
        existing_nodes = [n for n in G.nodes() if n != new_node]
        
        if degrees.sum() > 0:
            probs = degrees / degrees.sum()
            targets = np.random.choice(existing_nodes, size=m, replace=False, p=probs)
        else:
            targets = np.random.choice(existing_nodes, size=m, replace=False)

        for target in targets:
            G.add_edge(new_node, target)

        if output == "snapshots": snapshots.append(G.copy())
    out=G
    if output=="snapshots":
        out=snapshots
    if output=="graph":
        out=G

    return out

#---------------------
# RANDOM WALK MODEL
#---------------------
def random_walk(N, m, p, directed=False, output="graph"):
    if output=="snapshots": snapshots=[]

    if directed: 
        G=nx.DiGraph()
    else:
        G=nx.Graph()
    G.add_nodes_from([*range(0,m)])

    for i in range(m):
        for j in range(i + 1, m):
            G.add_edge(i, j)

    next_node = m

    while next_node < N:
        G.add_node(next_node)
        #first link is wired to an old node chosen at random.
        #no loops
        old_node = np.random.choice(list(G.nodes()))
        while old_node == next_node: 
            old_node = np.random.choice(list(G.nodes()))
        G.add_edge(next_node, old_node)

        attached_nodes = set([old_node])
        #Each other link is attached to a randomly selected neighbor of old node, 
        #with probability p, or to another randomly selected node, with probability 1-p
        while len(attached_nodes) < m:
            if np.random.rand() < p and len(list(G.neighbors(old_node))) > 0:
                neighbors = list(G.neighbors(old_node))
                new_target = np.random.choice(neighbors)
            else:
                new_target = np.random.choice(list(G.nodes()))
            #no loops/repeats
            if new_target != next_node and new_target not in attached_nodes:
                G.add_edge(next_node, new_target)
                attached_nodes.add(new_target)

        if output == "snapshots": snapshots.append(G.copy())
        next_node += 1

    out=G
    if output=="snapshots":
        out=snapshots
    if output=="graph":
        out=G

    return out
