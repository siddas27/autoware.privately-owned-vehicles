from .backbone import Backbone
from .depth_supervision import DepthSupervision
from .scene_context import SceneContext
from .depth_neck import DepthNeck
from .super_depth_head import SuperDepthHead
import torch.nn as nn

class SuperDepthNetwork(nn.Module):
    def __init__(self):
        super(SuperDepthNetwork, self).__init__()
        
        # Encoder
        self.Backbone = Backbone()

        # Depth Supervision
        self.DepthSupervision = DepthSupervision()

        # Context
        self.SceneContext = SceneContext()

        # Neck
        self.DepthNeck = DepthNeck()

        # Depth Head
        self.SuperDepthHead = SuperDepthHead()
    

    def forward(self, image, pyramid_depth_features):
        features = self.Backbone(image)
        depth_supervision_features = self.DepthSupervision(pyramid_depth_features)
        deep_features = features[4]
        context = self.SceneContext(deep_features)
        neck = self.DepthNeck(context, features, depth_supervision_features)
        prediction, boundary = \
            self.SuperDepthHead(neck, features, depth_supervision_features)
        return prediction, boundary