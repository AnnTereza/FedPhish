import torch as T
from torch import nn, optim
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader, random_split
import numpy as np
import pandas as pd

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
  
def classify(features):
  '''
    Function to predict whether phishing or not using the features

    Returns True if the website is phishing, False otherwise
  '''

  # Load the model 
  pnn = T.load("PhishingClassifier1")

  # Create tensor
  features = T.tensor(features).double()

  # Classifiy the website
  if T.round(pnn(features))[0] == 0:
    pred = True
  else:
    pred = False
  
  return pred
