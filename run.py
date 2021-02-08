import json
import argparse
from src.data_loader import data_loader
from src.n_GCN import n_hidden_GCN
import pandas as pd
import numpy as np
import networkx as nx
import random

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dropout, Dense
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, Callback
import tensorflow as tf
from tensorflow.keras.regularizers import l2
from spektral.layers import GraphConv
import pathlib

def main():
    # Training settings
    local_path = str(pathlib.Path().parent.absolute())
    local_data = local_path + '/data'
    local_output = local_path + '/config/model-output.json'
    parser = argparse.ArgumentParser(description='Running model')
    parser.add_argument('--model', type=str, default='graph', choices=['n_GCN', 'graphsage'],
                        help='model to use for training (default: 2layerGNN)')
    parser.add_argument('--dataset', type=str, default='data1', choices=['data1'],
                        help='data set type (default data1 and only support data1 now)')
    parser.add_argument('--output_path', type=str, default=local_output,
                        help='path for the output json file')
    parser.add_argument('--agg_func', type=str, default='MEAN', choices=['MEAN', 'MAX'],
                        help='aggregate functions used in graphsage dafault is mean')
    parser.add_argument('--num_neigh', type=int, default=10,
                        help='Number of neighbors used in graphsage default is 10')
    parser.add_argument('--n', type=int, default=0,
                        help='Number of hidden layers if the model is n_GCN')
    parser.add_argument('--self_weight', type=float, default=10,
                        help='The weight of selp loop if the model is n_GCN')
    parser.add_argument('--hidden_neurons', type=int, default=200,
                        help='hidden neurons in hidden layer (GCN) (default: 200)')
    parser.add_argument('--device', type=str, default='cuda',
                        help='Device for trianing the model (dafault: cuda)')
    parser.add_argument('--epochs', type=int, default=50,
                        help='number of epochs to train (default: 50)')
    parser.add_argument('--lr', type=float, default=1e-3,
                        help='learning rate (default: 1e-3)')
    parser.add_argument('--val_size', type=float, default=0.3,
                        help='Validtion size (default: 0.3)')
    parser.add_argument('--Lambda', type=float, default=0.3,
                        help='Lambda used in LPA-GCN model (default: 0.3)')
    parser.add_argument('--test', action = 'store_true', help='running test')
    args = parser.parse_args()
    if args.test:
        with open('test/testdata/test.json') as f:
             data = json.load(f)
        X, y, A = np.array(data['X']), np.array(data['y']), np.array(data['A'])
        model = n_hidden_GCN(A, X, y, 0)
        hist = model.train_model()
    else:
        if args.dataset == 'data1':
            loader = data_loader("../data/voting_features.csv", "../data/edges.csv")
            X, y, A = loader.get_train()
            if args.model == 'n_GCN':
                model = n_hidden_GCN(A,X,y, N=args.n, hidden_neurons=args.hidden_neurons, self_weight=args.self_weight, val_size=args.val_size)
                hist = model.train_epoch(epochs=args.epochs, lr=args.lr)
            if args.model == 'graphsage':
                model = GraphSage(A, X, y, device=args.device, agg_func=args.agg_func, hidden_neuron=args.hidden_neurons, len_walk=args.len_walk, num_neigh=args.num_neigh, val_size=args.val_size)
                hist = model.train_epoch(epochs = args.epochs, lr=args.lr)
        else:
            loader = arxiv_loader(seed=args.seed, size=args.arxiv_size)
            A, X, y = loader.get_train()
            if args.model == 'n_GCN':
                model = n_hidden_GCN(A,X,y, N=args.n, hidden_neurons=args.hidden_neurons, self_weight=args.self_weight, val_size=args.val_size, F=128, class_number=len(set(y)))
                hist = model.train_epoch(epochs=args.epochs, lr=args.lr)
            if args.model == 'graphsage':
                model = GraphSage(A, X, y, device=args.device, agg_func=args.agg_func, hidden_neuron=args.hidden_neurons, len_walk=args.len_walk, num_neigh=args.num_neigh, val_size=args.val_size,  F=128, class_num=len(set(y)))
                hist = model.train_epoch(epochs = args.epochs, lr=args.lr)
    with open(args.output_path, 'w') as f:
            json.dump(hist, f)
        
if __name__ == '__main__':
    main()
    # Examples:
    # python run.py --model graph --dataset cora