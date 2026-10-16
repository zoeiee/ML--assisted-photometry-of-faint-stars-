import torch
from torch import nn
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.AvgPool2d(2),nn.Conv2d(8,16,3,padding=1),nn.ReLU(),nn.AvgPool2d(2),nn.Flatten(),nn.Linear(16*8*8,32),nn.ReLU(),nn.Linear(32,1))
    def forward(self,x):return self.net(x).flatten()
def inputs(images):
    # Per-observation edge median: available at inference, no population/test fit.
    edge=torch.cat([images[:,0,:],images[:,-1,:],images[:,:,0],images[:,:,-1]],dim=1)
    b=edge.median(dim=1).values
    return ((images-b[:,None,None])/100.)[:,None]
