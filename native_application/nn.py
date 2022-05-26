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