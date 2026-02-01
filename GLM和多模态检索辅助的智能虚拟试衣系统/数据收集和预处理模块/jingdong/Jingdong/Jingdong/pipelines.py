import os

import requests
from itemadapter import ItemAdapter
import pymysql

class jd001:
    def process_item(self, item, spider):
        print(item)
        print("******************")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='TB01')
        cursor = conn.cursor()
        sql22 = "select * from T恤 where id = (select max(id) from T恤);"

        cursor.execute(sql22)
        # 获取所有记录列表
        results = cursor.fetchall()
        count2 = results[0][0]
        print(count2)
        #print(count2)
        #print(tt)
        sql111 = '''INSERT INTO T恤(ID,NAME,PRICE, SHOPLINK, PICLINK)
                values('%s','%s','%s','%s','%s')'''

        count2 = count2 + 1
        print(count2, item['title'], item['price'], item['shoplink'], item['img_url'])
        try:
            print('开始写入')
            cursor.execute(sql111 % (count2, item['title'], item['price'], item['shoplink'], item['img_url']))
            conn.commit()
        except:
            print('写入数据库失败')
        cursor.close()
        #conn.close()


        root = "T恤//"  # 保存图片的根目录
        path = root + '' + str(count2) + ".jpg"  # 图片的名称
        try:
            if not os.path.exists(root):  # 判断文件夹是否存在
                os.mkdir(root)  # 不存在则创建文件夹
            r = requests.get(item['img_url'], timeout=3)  # 获取图片的内容
            # print(r)
            with open(path, 'wb') as f:
                f.write(r.content)  # 保存
                f.close()
        except:
            print("爬取失败")