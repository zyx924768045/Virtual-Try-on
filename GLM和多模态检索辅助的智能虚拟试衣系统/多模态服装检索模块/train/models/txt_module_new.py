import torch
from torch import nn
from torch.nn import functional as F
# from models.basic_module import BasicModule
from basic_module import BasicModule
import numpy as np
LAYER1_NODE = 8192
tags = np.load(r'D:\毕业设计\Graduation_project_core\data\FLICKR-25k_texts.npy')[:100].astype('float')
print(tags.shape)
tags = torch.from_numpy(tags).unsqueeze(1).unsqueeze(-1).type(torch.float)
# x = x.squeeze(0)
# x = F.avg_pool1d(x,kernel_size=5,stride=5,padding=0)
# print(x.shape)
# x = nn.Conv2d(x,in_channels=1,out_channels=1,stride=1,padding=0)
# print(x.shape)
class MultiScaleTxt(BasicModule):
    def __init__(self):
        super(MultiScaleTxt, self).__init__()
        self.Conv1 = nn.Conv2d(1,1,kernel_size=(1, 1) ,stride=(1, 1),padding=0)
        self.Conv2 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv3 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv4 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv5 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv6 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
    def forward(self,x):
        print('x.shape',x.shape)
        x1 = F.avg_pool2d(x,kernel_size=[5,1],stride=[5,1],padding=0)
        x1 = self.Conv1(x1)
        x1 = F.relu(x1)
        print(x1.shape)
        x2 = F.avg_pool2d(x, kernel_size=[10, 1], stride=[10, 1], padding=0)
        x2 = self.Conv2(x2)
        x2 = F.relu(x2)
        print(x2.shape)
        x3 = F.avg_pool2d(x, kernel_size=[15, 1], stride=[15, 1], padding=0)
        x3 = self.Conv3(x3)
        x3 = F.relu(x3)
        print(x3.shape)
        x4 = F.avg_pool2d(x, kernel_size=[15, 1], stride=[15, 1], padding=0)
        x4 = self.Conv4(x4)
        x4 = F.relu(x4)
        print(x4.shape)
        x5 = F.avg_pool2d(x, kernel_size=[30, 1], stride=[30, 1], padding=0)
        x5 = self.Conv5(x5)
        x5 = F.relu(x5)
        print(x5.shape)
        x6 = F.avg_pool2d(x, kernel_size=[50, 1], stride=[30, 1], padding=0)
        x6 = self.Conv6(x6)
        x6 = F.relu(x6)
        x = torch.cat((x,x1,x2,x3,x4,x5,x6),dim=-2)
        print(x6.shape)
        print('x.shape',x.shape)
        # print(x6.shape)

# net = MultiScaleTxt()
#
# net.forward(tags)

def weights_init(m):
    if type(m) == nn.Conv2d:
        nn.init.normal_(m.weight.data, 0.0, 0.01)
        nn.init.normal_(m.bias.data, 0.0, 0.01)
        # nn.init.normal_(m.bias.data, 0.0, 0.01)


class TxtModule(BasicModule):
    def __init__(self, y_dim, bit):
        """
        :param y_dim: dimension of tags
        :param bit: bit number of the final binary code
        """
        super(TxtModule, self).__init__()
        self.module_name = "text_model"
        # self.MultiScaleTxt = nn.Sequential(
        #     F.avg_pool2d()
        # )

        self.Conv1 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv2 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv3 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv4 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv5 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        self.Conv6 = nn.Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1), padding=0)
        # full-conv layers
        self.conv1 = nn.Conv2d(1, LAYER1_NODE, kernel_size=(2076, 1), stride=(1, 1))
        self.conv2 = nn.Conv2d(LAYER1_NODE, bit, kernel_size=1, stride=(1, 1))

        self.apply(weights_init)

    def forward(self, x):
        x1 = F.avg_pool2d(x, kernel_size=[5, 1], stride=[5, 1], padding=0)
        x1 = self.Conv1(x1)
        x1 = F.relu(x1)
        print(x1.shape)
        x2 = F.avg_pool2d(x, kernel_size=[10, 1], stride=[10, 1], padding=0)
        x2 = self.Conv2(x2)
        x2 = F.relu(x2)
        print(x2.shape)
        x3 = F.avg_pool2d(x, kernel_size=[15, 1], stride=[15, 1], padding=0)
        x3 = self.Conv3(x3)
        x3 = F.relu(x3)
        print(x3.shape)
        x4 = F.avg_pool2d(x, kernel_size=[15, 1], stride=[15, 1], padding=0)
        x4 = self.Conv4(x4)
        x4 = F.relu(x4)
        print(x4.shape)
        x5 = F.avg_pool2d(x, kernel_size=[30, 1], stride=[30, 1], padding=0)
        x5 = self.Conv5(x5)
        x5 = F.relu(x5)
        print(x5.shape)
        x6 = F.avg_pool2d(x, kernel_size=[50, 1], stride=[30, 1], padding=0)
        x6 = self.Conv6(x6)
        x6 = F.relu(x6)
        x = torch.cat((x, x1, x2, x3, x4, x5, x6), dim=-2)
        print('x.shape',x.shape)
        x = self.conv1(x)
        print(x.shape)
        x = F.relu(x)
        x = self.conv2(x)
        print(x.shape)
        x = F.relu(x)
        # # x = self.conv3(x)
        # print(x.shape)
        x = x.squeeze()
        print(x.shape)
        return x
y_dim = tags.shape[1]
txt_net = TxtModule(y_dim,64)
txt_net.forward(tags)
