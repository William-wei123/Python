# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import torch
import torchvision
import numpy as np
import sys

import matplotlib.pyplot as plt

batch_size = 256

#获取数据集，主要用.datasets()
Fashtrain_iter = torchvision.datasets.FashionMNIST(root='~/Datasets/FashionMNIST',train=True,download=True,transform=torchvision.transforms.ToTensor())#自动下载数据集
Fashtest_iter = torchvision.datasets.FashionMNIST(root='~/Datasets/FashionMNIST',train=False,download=True,transform=torchvision.transforms.ToTensor())

#

#按批量处理数据
def Load_data_fas_mnist(batch_size):
    # 加载小批量数据用torch.utils.data.DataLoader()
    train_iter = torch.utils.data.DataLoader(Fashtrain_iter,batch_size=batch_size,shuffle=True)
    test_iter = torch.utils.data.DataLoader(Fashtest_iter,batch_size=batch_size,shuffle=True)
    return train_iter,test_iter

#获得label标签
def get_fas_mnist_labels(labels):        #labels是一个数字列表，返回对应的实物
    text_lab = ['t-shirt','trouser','pullover','dress','coat','sandal','shirt','sneaker','bag','ankle boot']
    return [text_lab[int(i)] for i in labels]       #因为labels是一个列表呢

#展示图片   img 为图片，lab 为标签  都要求是列表
def Show_Fashion_mnist(img,lab):
    _, figs = plt.subplots(1, len(img),figsize=(12,12))     #figsize   是指图表的大小
    for f,image,lbl in zip(figs,img,lab):       # 打包为元组的列表      在想，为什么不直接赋值
        f.imshow(image.view((28,28)).numpy())       #28x28是指每个图片的像素宽度
        f.set_title(lbl)
    plt.show()
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

num_input,num_output,num_hiddens = 784,10,256           #28*28=784    10种类别       只有一层隐藏层输入是256
#设定模型
net = torch.nn.Sequential(torch.nn.Linear(num_input,num_hiddens),
                          torch.nn.ReLU(),
                          torch.nn.Linear(num_hiddens,num_output),
                          torch.nn.ReLU(),
                          )
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    X, Y = [], []
    #print(Fashtrain_iter)
    #print(Fashtest_iter)
    for i in range(10):
        X.append(Fashtrain_iter[i][0])
        Y.append(Fashtest_iter[i][1])
        #Show_Fashion_mnist(train_iter[i][0],test_iter[i][1])
    Show_Fashion_mnist(X, get_fas_mnist_labels(Y))

    train_iter,test_iter = Load_data_fas_mnist(batch_size=256)

    print(test_iter)
    print(net)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
