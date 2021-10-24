import torch
from torchvision import datasets, transforms
from .model import CSRNet
from .dataset import *

def CreateModel():
    model = CSRNet()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-7, momentum=0.95)

    checkpoint = torch.load("0checkpoint.pth.tar")
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    # Optional
    epoch = checkpoint["epoch"]
    loss = checkpoint["loss"]

    model.eval()
    return model

def ProcessData(path):
    loader = torch.util.data.DataLoader(
        dataset.listDataset(list(path), transform=transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224,0.225]),
            ]), train=False,
        batch_size=1)
    )
    return loader


def RunModel(path):
    
    """
        params:
        path: input image path
    """
    CSRNet = CreateModel()
    loader = ProcessData(path)
    for img in loader:
        output = CSRNet.forward(img)
    return output.data.sum()