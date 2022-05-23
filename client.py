from collections import OrderedDict
import pandas as pd
import torch
import torch as T
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader, random_split

import numpy as np
import flwr as fl


DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class PhishingClassifierNN(nn.Module):
  def __init__(self):
    super().__init__()
    self.input = nn.Linear(21, 64)
    self.hidden1 = nn.Linear(64, 64)
    self.hidden2 = nn.Linear(64, 64)
    self.output = nn.Linear(64, 1)
    
  def forward(self, x):
    x = F.relu(self.input(x))  
    x = F.relu(self.hidden1(x))
    x = F.relu(self.hidden2(x))
    x = T.sigmoid(self.output(x))
    return x


def load_data():
  # Load data from csv files
  df = pd.read_csv("dataset.csv")
  df = df.drop("Unnamed: 0", axis=1)
  X = df.drop("Result", axis=1)
  print(X.columns)
  y = df["Result"]

  # Convert them to tensors
  features = T.tensor(X.values.astype(np.float64))
  target = T.tensor(y)

  # Create PyTorch Dataset
  phishingDS = TensorDataset(features, target.to(T.float64))

  # Split the dataset
  trainSize = int(0.8*len(phishingDS))
  testSize = len(phishingDS) - trainSize
  trainSet, testSet = random_split(phishingDS, [trainSize, testSize])

  # Create PyTorch DataLoader
  trainLoader = DataLoader(trainSet, batch_size=10, shuffle=True)
  testLoader = DataLoader(testSet, batch_size=10, shuffle=False)
    
  num_examples = {"trainset" : len(trainSet), "testset" : len(testSet)}
  return trainLoader, testLoader, num_examples


def train(pnn, trainLoader, epochs):
  '''
    Training the neural network for epochs time using the data
  '''
  loss_fn = nn.BCELoss()
  opt = torch.optim.Adam(pnn.parameters(), lr=0.0001)
  for epoch in range(epochs):
    for X,y in trainLoader:
      # 1. Generate predictions
      pred = pnn(X)

      # 2. Calculate loss
      loss = loss_fn(pred, y.reshape(y.size()[0], 1))
    
      # 3. Compute gradients
      loss.backward()
    
      # 4. Update parameters using gradients
      opt.step()
      
      # 5. Reset the gradients to zero
      opt.zero_grad()
    print(loss)


def test(pnn,testloader):
  '''
    Validating the model on the dataset
  '''
  loss_fn = nn.BCELoss()
  correct, total, loss = 0, 0, 0.0
  with T.no_grad():
    for X,y in testloader:
      output = T.round(pnn(X))
      loss += loss_fn(output, y.reshape(y.size()[0], 1)).item()
      for idx, i in enumerate(output):
        if i == y[idx]:
          correct += 1
        total += 1
  accuracy = correct / total
  return loss, accuracy

# Initiate Network
pnn = PhishingClassifierNN().double().to(DEVICE)

# Load data
trainloader, testloader, num_examples = load_data()

# Flower client
class PhishingClient(fl.client.NumPyClient):
    def get_parameters(self):
        return [val.cpu().numpy() for _, val in pnn.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(pnn.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        pnn.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        train(pnn, trainloader, epochs=1)
        return self.get_parameters(), num_examples["trainset"], {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = test(pnn, testloader)
        return float(loss), num_examples["testset"], {"accuracy": float(accuracy)}

# Start flower client
fl.client.start_numpy_client("[::]:8080", client=PhishingClient())
