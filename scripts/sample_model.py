import torch
import torch.nn as nn


class SimpleFCNet(nn.Module):
    def __init__(self, in_features: int = 128, hidden: int = 64, out_features: int = 10):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden)
        self.act1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden, out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)
        x = self.act1(x)
        x = self.fc2(x)
        return x
