import pandas as pd

import src.config as config
import src.mysql_operating as mysql_operating


PG_HOST = config.PG_HOST
PG_PORT = config.PG_PORT
PG_USER = config.PG_USER
PG_PASSWORD = config.PG_PASSWORD
PG_DATABASE = config.PG_DATABASE

def read_directory(directory_name):
    array_of_img = []
    id_data=[]
    # this loop is for read each image in this foder,directory_name is the foder name with images.
    for filename in os.listdir(r"./"+directory_name):
        #print(filename) #just for test
        i=0
        #img is used to store the image data
        img = cv2.imread(directory_name + "/" + filename)
        array_of_img.append(img)
        #print(img)
        i=i+1
        id_data.append(i)
    return id_data,array_of_img
import os
import cv2
def read_picture(old_picture_file_name, new_picture_file_name):

    id_data=[]
    i = 0 #用来计算该文件夹中的图片数

    for pic_name in os.listdir(old_picture_file_name):
        img = cv2.imread(old_picture_file_name + "/" +pic_name, cv2.IMREAD_UNCHANGED)
        pic_height, pic_width, channel = img.shape
        if pic_width >= pic_height:
            cv2.imwrite(new_picture_file_name + "/" + str(i) + ".png", img)
        i = i + 1
        id_data.append(i)
    return id_data



def clear_db():
    conn = mysql_operating.connect_mysql_server(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
    mysql_operating.execute_del(conn)
    conn.commit()
    conn.close()


def store_db(data):
    conn = mysql_operating.connect_mysql_server(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
    mysql_operating.execute_insert(conn,data)

def image_db(ids):
    id2title_map = {}
    conn = mysql_operating.connect_mysql_server(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
    out_put = mysql_operating.search_in_mysql(conn,ids)

    for i,data in enumerate(out_put):
        _id,image = data
        id2title_map[_id] = image
    return id2title_map
