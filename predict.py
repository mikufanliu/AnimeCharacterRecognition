# -*- coding=utf-8 -*-
from imageai.Prediction.Custom import CustomImagePrediction
import os
import json

'''预测图片'''

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

IMAGE_PATH = "uploader/80.jpg"  # 测试图片路径
MODEL_PATH = "data/models/model_ex-150_acc-0.883871.h5"  # 模型路径
JSON_PATH = "data/json/model_class.json"  # json文件路径
RESULT_COUNT = 3  # 显示预测结果的数量

prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()  # 设置ResNet模型


def predict(img_path, model_path=MODEL_PATH, json_path=JSON_PATH, result_count=RESULT_COUNT):
    if not os.path.exists(img_path):
        print("Can not found img %s" % img_path)
        return

    with open(json_path) as f:
        num_obj = len(json.load(f))
        print(num_obj)

    prediction.setModelPath(model_path)
    prediction.setJsonPath(json_path)
    prediction.loadModel(num_objects=num_obj)
    predictions, probabilities = prediction.predictImage(img_path, result_count=result_count)

    result = {}
    i = 1
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        result[i] = {eachPrediction: str(round(float(eachProbability), 2)) + '%' }
        i = i + 1

    print(result)
    return result


def main():
    result = predict(IMAGE_PATH, MODEL_PATH, JSON_PATH, RESULT_COUNT)
    # print(result)


if __name__ == "__main__":
    main()
