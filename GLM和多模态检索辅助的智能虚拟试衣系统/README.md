自有数据集典型样本文件夹文件目录如下：
|-电商服装数据集
|-中文穿搭推荐文本对话数据集（只传了json格式）

虚拟换衣模块文件目录如下所示：
|-docker                      #docker文件夹,用于创建docker镜像和容器
    |-docker-compose.yaml         #部署应用
    |-Dockerfile                  #定制镜像
|-Interation	#FLASK文件
  |-pasta-gan-plusplus          #项目主文件夹
        |-_pycache_
    |-checkpoints                 #存放项目预训练模型，这里因为模型过大打包在“部分模型文件.rar”中
            |-pasta-gan++
         |-network-snapshot-004408.pkl 
    |-dnnlib          
    |-graphonomy                  #用于人体解析（分割），这里因为模型过大打包在“部分模型文件.rar”中
      |-data                        #存放用于人体解析的模型
         |-pretrained_model 
           |-inference.pth               
    |-metrics                     #定量计算模型效果               
    |-prep                        #数据预处理文件
            |-make_paires.py
      |-preprocessor.py
      |-resize_image.py
    |-pretrained_models           #存放openpose（人体关键点检测）的模型，这里因为模型过大打包在“部分模型文件.rar”中
      |-pose_deploy_linevec.prototxt
      |-pose_iter_440000.caffemodel             
        |-test_results                #存放虚拟试衣结果图像 `cd test_results/full && ls`
      |-full                          查看结果  
      |-lower
      |-upper 
    |-test_samples                #存放用于虚拟试衣的数据集及预处理后的图像 
      |-image
      |-keypoints
      |-parsing
    |-torch_utils
    |-traning                     #训练网络所需的文件（包括深度网络、数据处理、损失函数等）
  |-calc_metrics.py        
  |-dataset_tool.py
  |-human_colormap.mat         #人体肤色数据
  |-legacy.py
  |-prep_img.py                #先执行`python prep_img.py`进行图像预处理 
  |-test.py
  |-test.sh                    #`bash tesh.sh 1/2/3` (1上身 2下身 3全身)
  |-train.py
  |-train.sh
  |-util_classes.py
  |-util_functions.py
|-setup.sh                  #自动生成所需的文件夹，包括数据集和预训练的模型

多模态服装检索模块文件目录如下所示：
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

智能穿搭推荐模块文件目录如下所示：
|-bilstm_crf	#-bilstm_crf模型文件、代码
|-ChatGLM-6B-main          #环境配置文件和demo程序代码
    |-.github
        |-ISSUE_TEMPLATE
    |-ptuning	#存放P-tuning微调运行文件
    |-api.py
    |-cli_demo.py	#命令行运行文件
    |-LICENSE
    |-MODEL_LICENSE
    |-requirements.txt
    |-utils.py
    |-web_demo.py		#局域网访问页面运行文件
    |-web_demo_old.py
    |-web_demo2.py		#公网访问页面运行文件
|-Interation	#FLASK文件
|-model		#模型文件和配置信息，其中较大的8个模型文件被打包进百度网盘同路径下“部分模型文件.rar”压缩包中
|-tuning dataset	#模型微调使用的典型数据集样本

数据收集与预处理文件目录如下所示：
|-Jingdong              #项目文件夹
   |-Jingdong           #项目目录
      |-items.py               #定义数据结构
      |-middlewares.py    #中间件
      |-pipelines.py          #数据处理
      |-settings.py            #全局配置
      |-spiders               
          |-__init__.py       #爬虫文件
          |-jd.py
   |-scrapy.cfg               #项目基本配置文件
|-预处理		#中文穿搭推荐文本对话数据集预处理运行文件
jingdong文件目录如下所示：
|-baiduzhidao              #项目文件夹
 |-baidu.py   #爬虫文件
 |-insert.py   #写入数据库
 |-newdatabase.py #新建数据库数据表

virtualTry-on文件夹为“随心配”智能虚拟换衣系统的项目文件夹。
该项目基于Vue 3 + Vite 4.3.0 开发。以下为文件说明：
1.node_modules文件夹为项目安装的依赖，由于它属于公共类库，此处没有上传，是一个空文件夹。如果要让该项目正常运行，需要先安装依赖。
2.public文件夹为公共资源文件夹，存放一些公共资源。
3.src文件夹为项目的部分静态js、css资源以及项目的核心vue文件，保障项目的核心功能正常运行。
4.“.gitignore”为git相关文件，用于项目版本控制和协作开发。
5.home.css、vtry-on.css、wear.css均属于项目不同模块的css样式表文件。
6.index.html为项目开发版本的网站入口。
7.package-lock.json和package.json为项目开发的配置文件，控制项目的基本信息、指令集和依赖。
8.vite.config.js为vite项目使用rollup工具打包的配置文件，决定了项目打包的处理参数，包括体积压缩、大文件拆分打包、分类打包。