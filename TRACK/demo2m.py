# Author:chen
# -*- codeing = utf-8 -*-
# @File  :demo2m.py
# @Time  :2022/3/31
# @Author:William
# @Software:PyCharm
import numpy as np
import pylab
###############改成二维###################
'''
观测量变成二维，(x,y),我们认为他是匀速运动？？？
是不是要换成二阶矩阵

'''
Vx = 1
Vy = Vx/1000
Zkkk = np.zeros([100, 2])
Zkkk[:, 0] = np.random.normal(0,0.3,size=100)       #x
Zkkk[:, 1] = np.random.normal(0,0.0005,size=100)       #y
print(Zkkk[:, 0])
for k in range(1,100):
    Zkkk[k, 0] = Zkkk[k, 0] + Vx*k
    Zkkk[k, 1] = Zkkk[k, 1] + Vy*k

Zkkk = np.array(Zkkk)
# pylab.figure()
# # valid_iter = range(1,n_iter) # Pminus not valid at step 0
# pylab.plot(Zkkk[:, 0],Zkkk[:, 1],label='the obvious')
# pylab.xlabel('x')
# pylab.ylabel('y')
# #pylab.setp(pylab.gca(),'ylim',[0,.01])
# pylab.show()
def kaermantest(Zk, R_temp, Q_temp):   #传入 观测值。。。。。暂无传入  (N,2)
    #参数初始化
    number = Zk.shape[0]  #得到观测数据个数，得到预测的次数，也是最终数据的长度？
    QindR = Q_temp/R_temp           #这个比值可以体现最终滤波的光滑度？
    A = [[1,0,1,0],             #4x4
         [0,1,0,1],
         [0,0,1,0],
         [0,0,0,1]]
    H = [[1,0,0,0],             #2x4
         [0,1,0,0]]
    A = np.array(A)
    AT = A.transpose()
    H = np.array(H)
    HT = H.transpose()
    R = np.eye(2)*(R_temp)    #测量噪声，越小认为测量的越准
    Q = np.eye(4) * Q_temp # process variance   预测噪声协方差矩阵   Q 和 R谁大就认为谁的误差大，更不相信谁
    P = np.zeros([number, 4, 4])   #误差矩阵预测
    K = np.zeros([number, 4, 2])  # gain or blending factor卡尔曼增益


    x = np.zeros([number, 4])   #实际     一行代表一个数据，实际使用是否需要转置

    print(x.shape)
    x[0,0:2] = Zk[0]
    x[:, 2] = Vx       #x轴速度  要改
    x[:, 3] = Vx/1000      #y轴速度  要改

    Xp = np.zeros([number, 4])               #Xp 为预测值
    Xp[0:2,0:2] = Zk[0:2]
    # Xp[:, 2] = x[:, 2]  # x轴速度  要改
    # Xp[:, 3] = x[:, 3]
    # pylab.figure()
    # # valid_iter = range(1,n_iter) # Pminus not valid at step 0
    # pylab.scatter(Zk[:, 0], Zk[:, 1], label='the obvious')
    # pylab.xlabel('x')
    # pylab.ylabel('y')
    # pylab.title('Zk')
    for k in range(1, number):    #认为匀速运动，A矩阵相乘
        x[k, :] = A.dot(x[k-1, :])     #认为是匀速运动    ？？？？？？？？？当前真实值？ 1x4
        #更新
        Xp[k, :] = A.dot(Xp[k-1, :])    #1x4
        P[k, :, :] = (A.dot(P[k, :, :])).dot(AT) + Q   #4x4
        P_temp = P[k, :, :]     #临时用作计算         #4x4
        print('P_temp11')
        print(Q)
        print(P_temp)
        #校正
        K[k] = P_temp.dot(HT.dot(np.linalg.pinv(H.dot(P_temp.dot(HT)) + R)))  #4x2      #Kg(k)=P(k|k-1)H'/[HP(k|k-1)H' + R]
        K_temp = K[k]           #临时用作计算 #4x2
        Xp[k] = Xp[k] + K_temp.dot(Zk[k] - H.dot(Xp[k]))        #4x4
        P[k, :, :] = (np.ones([4, 4]) - K_temp.dot(H)).dot(P_temp)           #4x4
        print('P_temp22')
        print(P_temp)

    #Z = Zk              #观测值，认为是传感器的值，就是最后框架出来的预测值中心点
    pylab.figure()
    # valid_iter = range(1,n_iter) # Pminus not valid at step 0
    pylab.scatter(Zk[:, 0], Zk[:, 1], label='the obvious Zk')
    # pylab.scatter(x[:, 0], x[:, 1],  label='the ture')
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.title('Zk&Xp')
    # pylab.setp(pylab.gca(),'ylim',[0,.01])


    # pylab.figure()
    # valid_iter = range(1,n_iter) # Pminus not valid at step 0
    # pylab.scatter(Xp[:, 0], Xp[:, 1], label='the pre')
    # pylab.xlabel('x')
    # pylab.ylabel('y')
    # # pylab.setp(pylab.gca(),'ylim',[0,.01])
    # pylab.figure()
    pylab.scatter(x[:, 0], x[:, 1], label='the obvious')
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.title(QindR)
    pylab.scatter(Xp[:, 0], Xp[:, 1], label='the pre')
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.show()

# kaermantest(Zkkk, 0.000005, 0.000003)
for i in range(50):
    kaermantest(Zkkk, 0.0000005, 0.00000001*i)