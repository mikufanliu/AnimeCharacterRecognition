# -*- coding:utf-8 -*-
import cv2
import os
from glob import glob

SRC = "predict"
DST = "test1"


def get_faces(src, dst, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    # Create classifier
    cascade = cv2.CascadeClassifier(cascade_file)

    count = 0
    files = [y for x in os.walk(src) for y in glob(os.path.join(x[0], '*.*'))]  # 妙啊,一句话得到一个文件夹中所有文件
    for image_file in files:
        image_file = image_file.replace('\\', '/')  # 解决Windows下的文件路径问题
        target_path = "/".join(image_file.strip("/").split('/')[1:-1])
        target_path = os.path.join(dst, target_path) + "/"

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        image = cv2.imread(image_file)
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
            filename = os.path.basename(image_file).split('.')[0]
            cv2.imwrite(
                os.path.join(target_path,  str(count) + ".jpg"),
                crop_img
            )
            count = count + 1
    print("get %d face(s)" % count)


def main():
    get_faces(SRC, DST)


if __name__ == '__main__':
    main()
