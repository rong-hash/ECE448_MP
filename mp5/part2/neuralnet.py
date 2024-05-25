# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
# Modified by Mahir Morshed for the spring 2021 semester
# Modified by Joao Marques for the fall 2021 semester
# Modified by Kaiwen Hong for the Spring 2022 semester

"""
This is the main entry point for part 2. You should only modify code
within this file and neuralnet.py -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm


class NeuralNet(nn.Module):
    def __init__(self, lrate, loss_fn, in_size, out_size):
        """
        Initializes the layers of your neural network.

        @param lrate: learning rate for the model
        @param loss_fn: A loss function defined as follows:
            @param x - an (N,D) tensor
            @param y - an (N,D) tensor
            @param l(x,y) an () tensor that is the mean loss
        @param in_size: input dimension
        @param out_size: output dimension

        For Part 2 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.layer1 = nn.Linear(in_size, 32)
        self.layer2 = nn.Linear(32, out_size)
        self.optimizer = optim.Adam(self.parameters(), lr=lrate)



    def forward(self, x):
        """Performs a forward pass through your neural net (evaluates f(x)).

        @param x: an (N, in_size) Tensor
        @return y: an (N, out_size) Tensor of output from the network
        """
        x = F.relu(self.layer1(x))
        x = self.layer2(x)
        return x

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y.

        @param x: an (N, in_size) Tensor
        @param y: an (N,) Tensor
        @return L: total empirical risk (mean of losses) at this timestep as a float
        """
        self.optimizer.zero_grad()  # Reset gradients
        y_pred = self.forward(x)    # Compute predictions
        loss = self.loss_fn(y_pred, y)  # Compute loss
        loss.backward()             # Compute gradients
        self.optimizer.step()       # Update parameters
        return loss.item()          # Return the loss value
    
    def to(self, device):
        self.layer1 = self.layer1.to(device)
        self.layer2 = self.layer2.to(device)
        return super(NeuralNet, self).to(device)


def fit(train_set, train_labels, dev_set, n_iter, batch_size=100):
    """ Fit a neural net. Use the full batch size.

    @param train_set: an (N, in_size) Tensor
    @param train_labels: an (N,) Tensor
    @param dev_set: an (M, in_size) Tensor
    @param n_iter: an int, the number of epoches of training
    @param batch_size: size of each batch to train on. (default 100)

    NOTE: This method _must_ work for arbitrary M and N.

    @return losses: array of total loss at the beginning and after each iteration.
            Ensure that len(losses) == n_iter.
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: a NeuralNet object
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    in_size = train_set.shape[1]
    out_size = 2  # Assuming binary classification problem
    lrate = 0.001
    loss_fn = nn.CrossEntropyLoss()

    net = NeuralNet(lrate, loss_fn, in_size, out_size).to(device)
    train_set = train_set.to(device)
    train_labels = train_labels.to(device)
    dev_set = dev_set.to(device)
    mean = train_set.mean()
    std = train_set.std()
    train_set = (train_set - mean) / std
    dev_set = (dev_set - mean) / std 
    losses = []

    for epoch in tqdm(range(n_iter)):
        for i in range(0, len(train_set), batch_size):
            batch_x = train_set[i:i + batch_size]
            batch_y = train_labels[i:i + batch_size]
            loss = net.step(batch_x, batch_y)
            losses.append(loss)
        if epoch % 20 == 0:
            print(f"Epoch {epoch + 1}/{n_iter}, Loss: {losses[-1]}")

    # Evaluation on development set
    dev_preds = net(dev_set)
    yhats = torch.argmax(dev_preds, dim=1).cpu().numpy()  # Convert to NumPy array for binary labels

    return losses, yhats, net

