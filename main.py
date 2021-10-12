# This is a sample Python script.
# -*- codeing = utf-8 -*-
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2;   #'opencv-python'
import os;


def save_img():
    video_path = r'G:\asus\Desktop\陈伟平\研究生前\Python\视频分成帧\test'
    ima_Save_path = r'G:\asus\Desktop\111\test' #图片保存路径，因为不能出现中文
    videos = os.listdir(video_path)#获取目录下所有文件名，是一个列表
    for video_name in videos:
        print(video_name)
        ###file_name = video_name.split('.')[0]
        rval = False;
        file_type = video_name.split('.')[-1]
        if( (file_type == 'mp4') or (file_type == 'MP4')):#判断是不是MP4文件，是才继续按帧提取
            folder_name = ima_Save_path + '\\' + video_name.split('.')[0]
            os.makedirs(folder_name, exist_ok=True)
            file_name = video_path + '\\' + video_name
            vc = cv2.VideoCapture(file_name)  # 读入视频文件
            c = 0
            rval = vc.isOpened()
        else:
            continue;#下面不干了，继续从for开始
        while rval:  # 循环读取视频帧
            c = c + 1
            rval, frame = vc.read()
            pic_path = folder_name + '/'
            if rval:
                cv2.imwrite(pic_path + video_name.split('.')[0] + '_' + str(c) + '.jpg', frame)  # 存储为图像,保存名为 文件夹名_数字（第几个文件）.jpg
                #cv2.imwrite的文件路径不能出现中文，避坑
                cv2.waitKey(1)
            else:
                break
        vc.release()
        print('save_success')
        print(folder_name)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
##程序入口
if __name__ == '__main__':
    print_hi('PyCharm');
    save_img();

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
