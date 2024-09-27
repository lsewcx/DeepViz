import torch

def getDevice():
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')