# -*- coding=utf-8 -*-
from imageai.Prediction.Custom import CustomImagePrediction
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

IMAGE_PATH = "test1/tr/3.jpg"
MODEL_PATH = "data/models/model_ex-049_acc-0.846154.h5"
JSON_PATH = "data/json/model_class.json"
NUM_OBJ = "3"  # 模型中对象的数量
RESULT_COUNT = "2"  # 显示预测结果的数量


def predict(img_path, model_path, json_path, num_obj, result_count="1"):
    execution_path = os.getcwd()
    if not os.path.exists(os.path.join(execution_path, img_path)):
        print("Can not found img %s" % os.path.join(execution_path, img_path))
        return

    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()  # 设置ResNet模型
    prediction.setModelPath(os.path.join(execution_path, model_path))
    prediction.setJsonPath(os.path.join(execution_path, json_path))
    prediction.loadModel(num_objects=num_obj)
    predictions, probabilities = prediction.predictImage(os.path.join(execution_path, img_path),
                                                         result_count=result_count)

    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction + " : " + eachProbability)


def main():
    predict(IMAGE_PATH, MODEL_PATH, JSON_PATH, NUM_OBJ, RESULT_COUNT)


if __name__ == "__main__":
    main()
