# -*-coding=utf-8-*-
from imageai.Prediction.Custom import ModelTraining
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 关闭tensorflow warning

DATA_PATH = "data2"
TRAIN_NUM = 50  # 训练次数
BATCH = 5   # 批次


def train(data_path, train_num, batch):
    if not os.path.exists(data_path):
        print("Train data path is not exists")
        return
    num_obj = len(os.listdir(os.path.join(data_path, "train")))

    model_trainer = ModelTraining()
    model_trainer.setModelTypeAsResNet()  # 训练的算法
    model_trainer.setDataDirectory(data_path)  # 训练的目录
    model_trainer.trainModel(num_objects=num_obj,  # 该参数用于指定图像数据集中对象的数量
                             num_experiments=train_num,  # 该参数用于指定将对图像训练的次数，也称为epochs
                             enhance_data=True,  # 该参数用于指定是否生成训练图像的副本以获得更好的性能
                             batch_size=batch,  # 该参数用于指定批次数量。由于内存限制，需要分批训练，直到所有批次训练集都完成为止
                             show_network_summary=True  # 该参数用于指定是否在控制台中显示训练的过程
                             )
    print('Model train finished')


def main():
    train(DATA_PATH, TRAIN_NUM, BATCH)


if __name__ == '__main__':
    main()

