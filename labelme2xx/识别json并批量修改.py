# Author:chen
# -*- codeing = utf-8 -*-
# @File  :识别json并批量修改.py
# @Time  :2021/12/3
# @Author:William
# @Software:PyCharm


# import module
import os
import json


def rest_rect(file_old, file_new):
    # filename_rest = os.listdir(file_old)  # 获取需要读取的文件的名字
    # L = []
    #
    # for rest in filename_rest:
    #     if os.apth.splitext(rest)[1]='.json':
    #         L.append(os.path.join(file_old, rest))  # 创建文件路径
    #
    # for f11 in L:

    if os.path.splitext(file_old)[1] == '.json':
        filename = file_old
        with open(filename, 'r+') as f:
            data = json.load(f)
            print(data['images'].__len__())
            for i in range(data['images'].__len__()):
                id = data['images'][i]['id']
                img_file_name = data['images'][i]['file_name']
                print(img_file_name)
                print(id)
                # img_file_name = '0'+str(300-1+id)
                data['images'][i]['file_name'] = '0'+str(300-1+id)+'.png'
                print(data['images'][i]['file_name'])
                print(type(data['images'][i]['file_name']))
            # data[0]['resType'] = 'rect'
            # newpath = os.path.join(file_new, os.path.split(f11)[1])
            # with open(newpath, 'w') as f2:
            #     json.dump(data, f2)  # 写入f2文件到本地
            with open(file_new, 'w') as f2:
                json.dump(data, f2)  # 写入f2文件到本地




# 函数调用
rest_rect('test.json', 'test1.json')
