# -*- coding:utf-8 -*-
import cv2
import os
from glob import glob
import numpy as np
import shutil

'''处理原图片得到人物脸部图片并按比例分配train和test用于训练模型'''

SRC = "Raw"  # 待处理的文件路径
DST = "data2"  # 处理后的文件路径
TRAIN_PER = 5  # train的图片比例
TEST_PER = 1  # test的图片比例


def rename_file(path, new_name="", start_num=0, file_type=""):
    if not os.path.exists(path):
        return
    count = start_num
    files = os.listdir(path)
    for file in files:
        old_path = os.path.join(path, file)
        if os.path.isfile(old_path):
            if file_type == "":
                file_type = os.path.splitext(old_path)[1]
            new_path = os.path.join(path, new_name + str(count) + file_type)

            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                count = count + 1
    # print("Renamed %d file(s)" % (count - start_num))


def get_faces(src, dst, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    # Create classifier
    cascade = cv2.CascadeClassifier(cascade_file)

    files = [y for x in os.walk(src) for y in glob(os.path.join(x[0], '*.*'))]  # 妙啊,一句话得到一个文件夹中所有文件

    for image_file in files:
        image_file = image_file.replace('\\', '/')  # 解决Windows下的文件路径问题
        target_path = "/".join(image_file.strip("/").split('/')[1:-1])
        target_path = os.path.join(dst, target_path) + "/"
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        count = len(os.listdir(target_path)) + 1

        image = cv2.imdecode(np.fromfile(image_file, dtype=np.uint8), -1)  # 解决中文路径读入图片问题
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.05,  # 指定每个图像缩放比例缩小图像大小的参数
                                         minNeighbors=4,  # 此参数将影响检测到的面孔。值越高，检测结果越少，但质量越高
                                         minSize=(24, 24)  # 最小对象大小。小于此值的对象将被忽略
                                         )
        for (x, y, w, h) in faces:
            crop_img = image[y:y + h, x:x + w]
            crop_img = cv2.resize(crop_img, (96, 96))  # 重置为96*96
            # filename = os.path.basename(image_file).split('.')[0]
            cv2.imencode('.jpg', crop_img)[1].tofile(os.path.join(target_path, str(count) + ".jpg"))

    print("All images are cropped")


def divide_train_test(src, train_percentage=5, test_percentage=1):
    if not os.path.exists(src):
        print("folder %s is not exist" % src)
        return
    dirs = os.listdir(src)

    test_dir = os.path.join(src, "test")
    train_dir = os.path.join(src, "train")
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)

    for dir_name in dirs:
        if dir_name != "test" and dir_name != "train":
            current_dir = os.path.join(src, dir_name)
            test_dir = os.path.join(src, "test", dir_name)
            train_dir = os.path.join(src, "train", dir_name)
            if not os.path.exists(test_dir):
                os.mkdir(test_dir)
            if not os.path.exists(train_dir):
                os.mkdir(train_dir)

            if os.path.isdir(current_dir):
                images = os.listdir(current_dir)
                image_num = len(images)
                for image in images:
                    filename = os.path.basename(image).split('.')[0]
                    if filename.isdigit():
                        percentage = train_percentage + test_percentage
                        test_num = (image_num / percentage) * test_percentage + 1
                        if int(filename) <= test_num:
                            if not os.path.exists(os.path.join(test_dir, image)):
                                shutil.move(os.path.join(current_dir, image), os.path.join(test_dir))
                            else:
                                os.remove(os.path.join(current_dir, image))
                        else:
                            if not os.path.exists(os.path.join(train_dir, image)):
                                shutil.move(os.path.join(current_dir, image), os.path.join(train_dir))
                            else:
                                os.remove(os.path.join(current_dir, image))
            shutil.rmtree(current_dir)

    for dirs in os.listdir(src):
        for name in os.listdir(os.path.join(src, dirs)):
            if os.path.isdir(os.path.join(src, dirs, name)):
                rename_file(os.path.join(src, dirs, name))

    print("Set all cropped images to train and test")


def main():
    get_faces(SRC, DST)
    divide_train_test(src=DST, train_percentage=TRAIN_PER, test_percentage=TEST_PER)


if __name__ == '__main__':
    main()
