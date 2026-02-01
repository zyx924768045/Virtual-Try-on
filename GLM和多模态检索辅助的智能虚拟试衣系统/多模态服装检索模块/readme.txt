# CLIP_FAISS

PyTorch implementataion for Deep cross-modal hashing


##  目录结构描述
    ├── ReadMe.md           // 帮助文档
    ├── Interation	//FLASK文件
    ├── Mysql   // 存储图像
        ├──mysql_operating.py
        ├──Open_images.py
        ├──Save_images_to_mysql.py
    ├── result             // 展示结果

    ├── src
        ├── config.py
        ├── data_utils.py
        ├── faiss_clip.py
    ├── train
        ├── checkpoints
        ├── models
            ├── _int_.py
            ├── basic_module.py
            ├── img_module.py
            ├── txt_module.py
            ├── txt_module_new.py
        ├──new_checkpoints
        ├──static
        ├── templates
    ├── Clip微调.py //对编码器进行微调
    ├── 测试一下.py  //测试模型是否能运行
    ├── 调用.py //对模型进行调用


## Environment

`python 3.5+`

`pytorch 0.3.0+`
## Usage

`mkdir checkpoints result` to create required folder.##创建所需文件夹

`python main.py help` to get help information.##获取帮助信息.

`python main.py train` for train and test DCMH.##用于训练和测试 CLIP_FAISS。

`python main.py test` for test only.##仅用于测试.
`python Clip微调.py` to encode images and test  meantime Fine tune##对图像和文本进行编码并同时进行微调
`python mysql_operating.py  `to hold image datasets##保存图像数据集
'python Open_images.py'to Open images database#读取图像数据库
'python data_utils.py'to processing data#处理图像、文本数据
`python 测试一下.py `to Test that the model can run##测试模型是否可以运行
` python faiss_clip.py`to uild the index file and look for it##使用索引文件并查找
## Dataset

*图片数据库：
* UPT_512_320
* jingdong