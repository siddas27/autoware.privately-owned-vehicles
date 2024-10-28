#! /usr/bin/env python3
import torch
import torch.nn as nn

class SceneContextTiny(nn.Module):
    def __init__(self):
        super(SceneContextTiny, self).__init__()
        # Standard
        self.GeLU = nn.GELU()
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(p=0.25)

        # Context - MLP Layers
        self.context_layer_0 = nn.Linear(1280, 800)
        self.context_layer_1 = nn.Linear(800, 800)
        self.context_layer_2 = nn.Linear(800, 200)

        # Context - Extraction Layers
        self.context_layer_3 = nn.Conv2d(1, 1280, 3, 1, 1)
    

    def forward(self, features):
        # Pooling and averaging channel layers to get a single vector
        feature_vector = torch.mean(features, dim = [2,3])

        # MLP
        c0 = self.context_layer_0(feature_vector)
        c0 = self.dropout(c0)
        c0 = self.GeLU(c0)
        c1 = self.context_layer_1(c0)
        c1 = self.dropout(c1)
        c1 = self.GeLU(c1)
        c2 = self.context_layer_2(c1)
        c2 = self.dropout(c2)
        c2 = self.sigmoid(c2)
        
        # Reshape
        c3 = c2.reshape([10, 20])
        c3 = c3.unsqueeze(0)
        c3 = c3.unsqueeze(0)
        
        # Context
        c4 = self.context_layer_3(c3)
        context = self.GeLU(c4)
        
        # Attention
        context = context*features + features
        return context   