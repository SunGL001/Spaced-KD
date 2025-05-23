"""resnet in pytorch



[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun.

    Deep Residual Learning for Image Recognition
    https://arxiv.org/abs/1512.03385v1
"""

import torch
import torch.nn as nn
import math

class BasicBlock(nn.Module):
    """Basic Block for resnet 18 and resnet 34

    """

    #BasicBlock and BottleNeck block
    #have different output size
    #we use class attribute expansion
    #to distinct
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()

        #residual function
        self.residual_function = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels * BasicBlock.expansion, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels * BasicBlock.expansion)
        )

        #shortcut
        self.shortcut = nn.Sequential()

        #the shortcut output dimension is not the same with residual function
        #use 1*1 convolution to match the dimension
        if stride != 1 or in_channels != BasicBlock.expansion * out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * BasicBlock.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * BasicBlock.expansion)
            )

    def forward(self, x):
        return nn.ReLU(inplace=True)(self.residual_function(x) + self.shortcut(x))

class BottleNeck(nn.Module):
    """Residual block for resnet over 50 layers

    """
    expansion = 4
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.residual_function = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, stride=stride, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels * BottleNeck.expansion, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels * BottleNeck.expansion),
        )

        self.shortcut = nn.Sequential()

        if stride != 1 or in_channels != out_channels * BottleNeck.expansion:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * BottleNeck.expansion, stride=stride, kernel_size=1, bias=False),
                nn.BatchNorm2d(out_channels * BottleNeck.expansion)
            )

    def forward(self, x):
        return nn.ReLU(inplace=True)(self.residual_function(x) + self.shortcut(x))

class ResNet(nn.Module):

    def __init__(self, block, num_block, num_classes=100):
        super().__init__()

        self.in_channels = 64

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True))
        #we use a different inputsize than the original paper
        #so conv2_x's stride is 1
        self.conv2_x = self._make_layer(block, 64, num_block[0], 1)
        self.conv3_x = self._make_layer(block, 128, num_block[1], 2)
        self.conv4_x = self._make_layer(block, 256, num_block[2], 2)
        self.conv5_x = self._make_layer(block, 512, num_block[3], 2)
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

    def _make_layer(self, block, out_channels, num_blocks, stride):
        """make resnet layers(by layer i didnt mean this 'layer' was the
        same as a neuron netowork layer, ex. conv layer), one layer may
        contain more than one residual block

        Args:
            block: block type, basic block or bottle neck block
            out_channels: output depth channel number of this layer
            num_blocks: how many blocks per layer
            stride: the stride of the first block of this layer

        Return:
            return a resnet layer
        """

        # we have num_block blocks per layer, the first block
        # could be 1 or 2, other blocks would always be 1
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            self.in_channels = out_channels * block.expansion

        return nn.Sequential(*layers)

    def forward(self, x):
        output = self.conv1(x)
        output = self.conv2_x(output)
        output = self.conv3_x(output)
        output = self.conv4_x(output)
        output = self.conv5_x(output)
        output = self.avg_pool(output)
        output_feature = output.view(output.size(0), -1)
        output = self.fc(output_feature)

        return output_feature, output

# def resnet18():
#     """ return a ResNet 18 object
#     """
#     return ResNet(BasicBlock, [2, 2, 2, 2])

# def resnet34():
#     """ return a ResNet 34 object
#     """
#     return ResNet(BasicBlock, [3, 4, 6, 3])

# def resnet50():
#     """ return a ResNet 50 object
#     """
#     return ResNet(BottleNeck, [3, 4, 6, 3])


class ResNet_downsample(nn.Module):

    def __init__(self, block, num_block, num_classes=100, downsample_factor=2):
        super().__init__()

        self.d = math.sqrt(downsample_factor)
        self.block_name = block.__name__

        self.in_channels = int(64/self.d)

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, int(64/self.d), kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(int(64/self.d)),
            nn.ReLU(inplace=True))
        #we use a different inputsize than the original paper
        #so conv2_x's stride is 1
        self.conv2_x = self._make_layer(block, int(64/self.d), num_block[0], 1)
        self.conv3_x = self._make_layer(block, int(128/self.d), num_block[1], 2)
        self.conv4_x = self._make_layer(block, int(256/self.d), num_block[2], 2)
        self.conv5_x = self._make_layer(block, int(512/self.d), num_block[3], 2)
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(int(512/self.d) * block.expansion, num_classes)

    @property
    def feature_size(self):
        if self.block_name =='BasicBlock':
            return int(512/self.d)
        elif self.block_name  =='BottleNeck':
            return int(512/self.d)*4

    def _make_layer(self, block, out_channels, num_blocks, stride):
        """make resnet layers(by layer i didnt mean this 'layer' was the
        same as a neuron netowork layer, ex. conv layer), one layer may
        contain more than one residual block

        Args:
            block: block type, basic block or bottle neck block
            out_channels: output depth channel number of this layer
            num_blocks: how many blocks per layer
            stride: the stride of the first block of this layer

        Return:
            return a resnet layer
        """

        # we have num_block blocks per layer, the first block
        # could be 1 or 2, other blocks would always be 1
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            self.in_channels = out_channels * block.expansion

        return nn.Sequential(*layers)

    def forward(self, x):
        output = self.conv1(x)
        output = self.conv2_x(output)
        output = self.conv3_x(output)
        output = self.conv4_x(output)
        output = self.conv5_x(output)
        output = self.avg_pool(output)
        output_feature = output.view(output.size(0), -1)
        # self.feature = output_feature
        output = self.fc(output_feature)

        return output_feature, output


def resnet18(downsample_factor=1):
    """ return a half-size ResNet 18 object
    """
    return ResNet_downsample(BasicBlock, [2, 2, 2, 2], downsample_factor=downsample_factor)


def resnet50(downsample_factor=1):
    """ return a ResNet 50 object
    """
    return ResNet_downsample(BottleNeck, [3, 4, 6, 3], downsample_factor=downsample_factor)


def resnet101(downsample_factor=1):
    """ return a ResNet 101 object
    """
    return ResNet_downsample(BottleNeck, [3, 4, 23, 3], downsample_factor=downsample_factor)

def resnet152(downsample_factor=1):
    """ return a ResNet 152 object
    """
    return ResNet_downsample(BottleNeck, [3, 8, 36, 3], downsample_factor=downsample_factor)


class spaced_distillation(nn.Module):
    def __init__(self,teacher,student):
        super(spaced_distillation, self).__init__()
        if teacher == 'resnet18':
            self.teacher = resnet18()
        elif teacher =='resnet50':
            self.teacher = resnet50()
        elif teacher =='resnet101':
            self.teacher = resnet101()
        elif teacher =='resnet152':
            self.teacher = resnet152()
        
        if student == 'resnet18':
            self.student = resnet18()
        elif student =='resnet50':
            self.student = resnet50()
        elif student =='resnet101':
            self.student = resnet101()
        elif student =='resnet152':
            self.student = resnet152()

        self.linear1 = nn.Linear(self.student.feature_size, int((self.student.feature_size+self.teacher.feature_size)/2))
        self.linear2 = nn.Linear(int((self.student.feature_size+self.teacher.feature_size)/2), self.teacher.feature_size)
        self.relu = nn.ReLU()

    def forward(self,x,obj):
        if obj=='teacher':
            feat_teacher, out_teacher =self.teacher(x)
            
        elif obj=='student':
            feat_student, out_student =self.student(x)

            feat_student = self.linear1(feat_student)
            feat_student = self.relu(feat_student)
            feat_student = self.linear2(feat_student)
        
        if obj=='teacher':
            return feat_teacher, out_teacher
        elif obj=='student':
            return feat_student, out_student


            








