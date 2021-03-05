# Political Analysis on Graph
 
### Project Description


### run.py
We implement the GCN and GraphSage models as our main models for training and comparison.

- parameters:
  - model: The choice of models. We only implement the GCN and GraphSage. 
  - dataset: The choice of datasets. There are multiple datasets, including data_voting, data_voting_senti, data_115. The differences between these datasets are features. The adjacency matrix of each dataset stays the same.
  - output_path: The output of project will be stored in json file.
  - agg_func: The choice of aggregated function in the graphSage model. We only support either MEAN or MAX. The default is MEAN.
  - num_neigh: The number of neighbors in the graphSage model. The default is 10.
  - n: The number of hidden layers in the GCN model. This can be tuned to reach higher accuracy.
  - self_weight: The weight of self-loop in the GCN model.
  - hidden_neurons: The number of hidden neurons in the GCN model. The default is 200 and it can be tuned to reach higher accuracy.
  - device: The device for training the model. We only support cuda.
  - epochs: The number of epochs for both models. The default is 200 epochs.
  - lr: The learning rate for both models. The default is 1e-4. This can be tuned for higher accuracy.
  - val_size: The size of testing data. The default is 0.3.
  - test: The parameter for running test data on models.

- some examples for using the project:
  - python run.py --test
  - python run.py --n_GCN
  - python run.py --dataset data_voting
  - python run.py --model n_GCN --n 2 --self_weight 20

  

# Our Project Website

Please view our website [here](https://anuragpamuru.github.io/dsc-180b-capstone-b03/)


### Contributers: 
Yimei Zhao, Anurag Pamuru, Yueting Wu
