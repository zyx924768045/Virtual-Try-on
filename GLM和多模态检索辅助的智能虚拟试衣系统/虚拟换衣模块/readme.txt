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