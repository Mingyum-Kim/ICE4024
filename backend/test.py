from io import BytesIO
import os
import cv2
import numpy as np
import pickle

# torch
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision import transforms

# loading model
MODEL_PATH = 'models/aram_model1.pt'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load(MODEL_PATH, map_location=device)
model.eval()

# Image preprocessing transformation to tensor
preprocess = transforms.Compose([  transforms.Resize([int(600), int(600)], interpolation=transforms.InterpolationMode.BOX),
                                            transforms.ToTensor(),
                                            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])    ])
                                    
testset = torchvision.datasets.ImageFolder(root = './uploads/model1', transform = preprocess)
testloader = DataLoader(testset, batch_size=2, shuffle=False, num_workers=0)

with torch.no_grad():
       for data, target in testloader:
           data, target  = data.to(device), target.to(device) 
           output1 = model(data)

what = output1.argmax(dim=1, keepdim=True)
print(what)
type(what)

mp = output1.argmax(dim=1, keepdim=True)[0][0].tolist()
print(mp)
