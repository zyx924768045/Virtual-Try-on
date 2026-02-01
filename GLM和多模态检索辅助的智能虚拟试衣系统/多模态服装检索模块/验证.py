from flask import Flask, render_template
import pymysql.cursors
import base64
import random
from io import BytesIO
from PIL import Image
conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
                           database='images')





# Get a random image from the database
with conn.cursor() as cursor:
    cursor.execute("select * from Images where id='1';")
    result = cursor.fetchone()
    image = result[1]
    print(image)
    # # 将二进制数据转换为图像对象
    # img = Image.open(BytesIO(image))
    # # 调整图像大小
    # img_resized = img.resize((256, 256))
    # # img_resized.save("resized_image.jpg")
    # img_bytes = BytesIO()
    # img_resized.save(img_bytes, format='JPEG')
    # img_binary = img_bytes.getvalue()
    # print(base64.b64encode(img_binary))
    # print(img_resized)



