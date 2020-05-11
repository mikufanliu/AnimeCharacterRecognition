# 动漫人物识别

本项目通过爬虫下载百度图片作为数据集，使用ImageAI训练模型，使用Flask作为后端进行在线展示。每一个部分均可独立使用，可自行准备数据集。项目结构说明如下：

1. 爬虫部分：

- `crawler.py`--获取百度图片真实地址

- `downloader.py`--下载图片

2. 数据处理部分：

- `rename_filename.py`--重命名文件

- `characters_name_list.txt`--下载人物名称

- `lbpcascade_animeface.xml`--切割人物脸部模型

- `get_faces.py`--切割获得人物脸部

3. 模型训练：

- `train.py`--训练模型

- `predict.py`--预测结果

4. 展示部分：

- `sever.py`--服务端

5. 文件夹说明

- `bin`--存放`phantomjs.exe`和`chromedriver.exe`

- `Raw`--存放爬虫下载文件

- `data`--存放训练结果和数据集

- `data/models`—-训练好的模型

- `data/json`—-模型相关的json文件

- `data/train`—-训练集

- `data/test`—-测试集

- `requirements`--存放需要的Python包列表

- `static`--前端静态文件

- `templates`--前端页面

- `uploader`--服务端存放用户上传文件