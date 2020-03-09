# -*- coding=utf-8 -*-
from imageai.Prediction.Custom import CustomImagePrediction
import os

'''预测图片'''

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

IMAGE_PATH = "predict/1.jpg"  # 测试图片路径
MODEL_PATH = "data2/models/model_ex-030_acc-0.400000.h5"  # 模型路径
JSON_PATH = "data2/json/model_class.json"  # json文件路径
NUM_OBJ = 5  # 模型中对象的数量
RESULT_COUNT = 2  # 显示预测结果的数量


def predict(img_path, model_path, json_path, num_obj, result_count=1):
    if not os.path.exists(img_path):
        print("Can not found img %s" % img_path)
        return

    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()  # 设置ResNet模型
    prediction.setModelPath(model_path)
    prediction.setJsonPath(json_path)
    prediction.loadModel(num_objects=num_obj)
    predictions, probabilities = prediction.predictImage(img_path, result_count=result_count)

    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction + " : " + eachProbability)


def main():
    predict(IMAGE_PATH, MODEL_PATH, JSON_PATH, NUM_OBJ, RESULT_COUNT)


if __name__ == "__main__":
    main()
