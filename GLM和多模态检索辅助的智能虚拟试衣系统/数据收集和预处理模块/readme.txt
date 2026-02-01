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
