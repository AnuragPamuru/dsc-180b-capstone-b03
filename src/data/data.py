import numpy as np
import networkx as nx
import pandas as pd
import torch

def get_adj(edges, directed):
    rows, cols = edges
    
    nodes = list(set(edges[0]).union(set(edges[1])))
    n_nodes = len(nodes)
    
    node_index = {}
    for i in np.arange(len(nodes)):
        node_index[nodes[i]] = i
        i += 1
    
    adj = np.zeros((n_nodes, n_nodes), dtype='float32')

    for i in range(len(edges)):
        adj[node_index[rows[i]], node_index[cols[i]]]  = 1.0
        if not directed: 
            adj[node_index[cols[i]], node_index[rows[i]]]  = 1.0 
            
    return adj

def get_data(feature_address, edges_address, directed = False):
    features = pd.read_csv(feature_address, sep ='\t', header=None)
    edges = pd.read_csv(edges_address, sep ='\t', header=None)

    #adjacency matrix
    adj = get_adj(edges, directed)
    
    
    labels = torch.LongTensor(features[-1])    
    features = np.array(features.iloc[:, 1:features.shape[1]-1])
    features = torch.FloatTensor(features)

    A = torch.from_numpy(adj).float()
    
    return features, labels, A
