from math import sqrt
import matplotlib.pyplot as plt
import torch
from torch import nn
import torch.nn.functional as F
from utils import *
import os
from loss import *
# from TridentUNet.TridentUNet import *
from DNANet.DNANet import *

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

class Net(nn.Module):
    def __init__(self, model_name, mode):
        super(Net, self).__init__()
        self.model_name = model_name
        self.cal_loss = SoftIoULoss()
        if model_name == 'DNANet':
            if mode == 'train':
                self.model = DNANet(mode='train')
            else:
                self.model = DNANet(mode='test')
        else:
            self.model = DNANet(mode='test')
    def forward(self, img, str1=None,str2=None):
        return self.model(img)

    def loss(self, pred, gt_mask):
        loss = self.cal_loss(pred, gt_mask)
        return loss
