import torch
from enum import Enum

class ModelCompute(Enum):
    Conv2d = 0
    Linear = 1

class Conv2dCompute():
    def __init__(self,input,output,kernal_size,stride,padding,dilation,groups,padding_mode,bias) -> None:
        self.input = input
        self.output = output
        self.kernal_size = kernal_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.groups = groups
        self.padding_mode = padding_mode
        self.bias = bias