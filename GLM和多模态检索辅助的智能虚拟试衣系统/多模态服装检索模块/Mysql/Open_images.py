import pymysql
from PIL import Image
conn = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='images')
cur = conn.cursor()
sql = "select * from Images where id='1';"
cur.execute(sql)
for image in cur.fetchall():
    print(image)
    with open('hhh.jpg','wb') as fb:
        fb.write(image[1])