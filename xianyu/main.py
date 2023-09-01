# Author:chen
# -*- codeing = utf-8 -*-
# @File  :main.py
# @Time  :2023/3/1 
# @Author:William
# @Software:PyCharm

def test_1(file_path="./raw/7.jpg", save_path = None, save_path_2= None,save_path_3 = None):
    import cv2
    import numpy as np
    import copy
    path = file_path#"./raw/8.jpg"
    img = cv2.imread(path)  # 导入并显示图像
    sp = img.shape  # 获得图像size
    print(sp[0], sp[1]) # 图像的长宽
    # cv2.imshow(file_path, img)

    lower = np.array([0, 0, 0])
    upper = np.array([0, 0, 0])
    mask = cv2.inRange(img, lower, upper) # 这里感觉不太对，之后优化一下，但这样可以实现，这里先记一下，之后记得改！！
    # ret, xy = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=1) # 创个kenel来腐蚀一下，这样好找

    collector = []
    contours, hierarchy = cv2.findContours(255-dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 每个点的轮廓找出来   找色块
    collector2 = np.array([])

    #直接导出所有255的坐标
    collector_index = np.argwhere(np.array(dilation)==255)
    i = 0
    img_2 = copy.deepcopy(img)
    for ind in range(np.max(sp)):
        if np.sum(np.argwhere(np.array(dilation[ind,:])==0)) >0:
            temp_row = np.argwhere(np.array(dilation[ind,:])==0)
            collector.append([ind,int(temp_row.mean())])
            cv2.circle(img_2,(int(temp_row.mean()),ind),2,(0,255,255))
            i = i+1
        pass
    print(i)
    # cv2.imshow("save_path_2", img_2)
    cv2.imwrite(save_path_2, img_2)

    collector_index = collector_index[:, [1,0]] #交换两列
    collector_np = np.array(collector)#除2
    collector_np = collector_np[:, [1, 0]]  # 交换两列
    # dot_collector = (collector_np) # 因为要用fitline 函数就要用到点集，所以这里用append创一个
    # output = cv2.fitLine(dot_collector, cv2.DIST_L2, 0, 0.01, 0.01)
    # k = output[1] / output[0]
    # b = output[3] - k * output[2]
    k ,b = poit2line(collector_np)
    # y1 = k * (0 - output[2]) + output[3]
    if len(contours) > 0:
        # cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和高

        boxes = [cv2.boundingRect(c) for c in contours]
        for box in boxes:

            x, y, w, h = box
            # 绘制矩形框对轮廓进行定位
            cv2.rectangle(img, (x, y), (x + w, y + h), (153, 153, 0), 2)
            if w*h<1000:
                continue
            # x1 = ((x+w/2)*k+b)
            cv2.rectangle(img, (x, y), (x + w, y + h), (153, 153, 0), 2)
            x1 = (y-b)/k
            x2 = (y + h-b)/k
            ptStart = (int(x1), y)
            ptEnd = (int(x2), y + h)
            # y = k * (0 - output[2]) + output[3]
            # x = (sp[1] - output[3]) / k + output[2] # 几个函数分别返回sinx, cosx, x0, yo, 刚好求斜率和直线经过的一点
            # print(x, y) # 前面我们有了图像的大小，刚好可以求截距，这样有了两个点，就可以画直线了
            # ptStart = (0, int(y))
            # ptEnd = (int(x), int(sp[1]))
            point_color = (0, 255, 255)  # BGR
            thickness = 10
            lineType = 4
            cv2.line(img, ptStart, ptEnd, point_color, thickness, lineType)


    cv2.imwrite(save_path_3, dilation)
    # cv2.imshow("colin", img)
    if save_path is None:
        pass
    else:
        cv2.imwrite(save_path, img)

    cv2.waitKey(0)
    print('')
    #对比1

    cv2.destroyAllWindows()


def poit2line(poits):
    import cv2
    dot_collector = poits  # 因为要用fitline 函数就要用到点集，所以这里用append创一个
    output = cv2.fitLine(dot_collector, cv2.DIST_L2, 0, 0.01, 0.01)
    k = output[1] / output[0]
    b = output[3] - k * output[2]
    return k,b
def Cal_kb_linear(data_line1):
    from scipy.optimize import leastsq

    X_line,Y_line = XY_line2Classifier_line(data_line1)
    r = leastsq(residuals, [1, 0], args=(X_line, Y_line))  # scipy.optimize.leastsq
    k, b = r[0]  # 最小二乘直线拟合的斜率和偏移
    return k,b

# 输出直线的X/Y坐标
def XY_line2Classifier_line(data_line1):
    import numpy as np
    X_line = []  # 存放分为同一类的直线的所有的x坐标
    Y_line = []  # 存放分为同一类的直线的所有的y坐标
    for line in data_line1:
        x1, y1, x2, y2 = line[0]
        X_line.append(x1), X_line.append(x2)
        Y_line.append(y1), Y_line.append(y2)
    X_line = np.array(X_line)
    Y_line = np.array(Y_line)
    return X_line,Y_line

#  直线拟合残差计算
def residuals(p, x, y_):
    k, b = p
    return y_ - (k * x + b)

if __name__ == '__main__':
    import os
    # test_1()
    pic_dir = './raw'
    save_dir = './after'
    if os.path.exists(save_dir) is False:
        os.makedirs(save_dir)
    for name in os.listdir(pic_dir):
        file_path = pic_dir + '/' + name
        save_path = save_dir + '/' + name
        save_path_2 = save_dir + '/xxx_' + name
        save_path_3 = save_dir + '/kenel_' + name
        test_1(file_path = file_path, save_path=save_path,save_path_2=save_path_2, save_path_3 = save_path_3)