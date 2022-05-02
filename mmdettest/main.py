from mmdet.apis import init_detector, inference_detector,show_result_pyplot
import os
from track.sort import *
from PIL import Image
import cv2  #用CV2显示并保存为视频
# import matplotlib.pyplot as plt
# #######################
# 使用什么跟踪算法 sort_flag
# 0:自己瞎写
# 1:sort
# 2：deepsort
# 3:?
from track.sort import *
sort_flag = 1
if sort_flag == 1:
    mot_tracker = Sort()
# ######################

# #######################
# 用于保存视频 save_mp4
# 0:no保存
# 1:保存
save_mp4 = 0

# ######################

ct_score = 0.3
def SET_COMPOSITOR(FILE_NAME):  #sort's key图像排序
    NUM = FILE_NAME.split("_")[-1]
    NUM = NUM.split(".")[0]
    return int(NUM)
def draw_result(img,reslut):
    print(img)
    # image = Image.open(img)
    image = cv2.imread(img)

    # figture = plt.figure(figsize=(16,9),dpi=120)
    # figture.imshow(image)
    # figture.axis('off')
    # # figture.title('result')
    # figture.imread
    for detection in reslut:
        x_min, y_min, x_max, y_max = detection[:4].astype(int)
        # figture.plot([x_min, x_min, x_max, x_max, x_min], [y_min, y_max, y_max, y_min, y_min], color='w', linewidth=0.5)
        Id = detection[4]
        # figture.text((x_min+x_max)/2,(y_min+y_max)/2, str(Id))
        # print(detection)
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 10)
        cv2.putText(image, str(Id), (x_min, y_min),cv2.FONT_HERSHEY_SIMPLEX,0.9, (0, 0, 255))
        # if save_mp4 == 1:

    # figture.show()
    return image


config_file = 'configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'
# download the checkpoint from model zoo and put it in `checkpoints/`
# url: https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth
checkpoint_file = 'checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'
device = 'cuda:0'
# init a detector
model = init_detector(config_file, checkpoint_file, device=device)
print(type(model))
# iference the demo image
dir_temp = '/home/xinqiang_329/桌面/cwp/snake/demo_images/MyData/MVI_1624_VIS/'
temp_img_list = os.listdir(dir_temp)
temp_img_list.sort(key=SET_COMPOSITOR)
if save_mp4 == 1:
    fps = 4
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_dir = 'output/%s.MP4'%os.path.split(os.path.split(dir_temp)[0])[1]#因为最后有/，所以多来一次
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, (1920, 1080))
for img in temp_img_list:
    img = dir_temp+img
    # img = '/home/xinqiang_329/桌面/cwp/snake/demo_images/MyData/MVI_1624_VIS'#'demo/derain_ret.png'   #MVI_1624_VIS_1.png
    result = inference_detector(model, img) #不经过训练，他默认的是分为80类，船好像在第8位（从0开始）
    # show_result_pyplot(model, img, result)
    ship_result = result[8] #boat 类在第8呢,而且里面包括分数很低的结果，需要过滤
    temp_ind = ship_result[:, 4] > ct_score
    # print(temp_ind)
    ship_result = ship_result[temp_ind, :]
    last_result = mot_tracker.update(ship_result)
    image_result = draw_result(img, last_result)
    if save_mp4==1:
        videoWriter.write(image_result)
    else:
        cv2.imshow('result',image_result)
        cv2.waitKey(5)

if save_mp4 == 1:
    videoWriter.release()

cv2.destroyAllWindows()

