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