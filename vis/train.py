from loguru import logger
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import TinyVGG
import torch.nn as nn
import torch.optim as optim
from utils.device import getDevice
from loguru import logger

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)

device = getDevice()
logger.info(f'Using device {device}')

model = TinyVGG().to(device)
# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train_model(num_epochs):
    model.train()
    for epoch in range(num_epochs):
        for data, target in train_loader:
            data, target = data.to(device), target.to(device)  # 将数据移动到 GPU
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

def train():
    global model
    train_model(2)
    model = model.to('cpu')
    torch.save(model, 'tinyvgg_model.pth')