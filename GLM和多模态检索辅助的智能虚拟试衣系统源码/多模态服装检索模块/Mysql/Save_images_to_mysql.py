import pymysql
import scipy.io as scio
import re
file = scio.loadmat('Data_preprocessing/mirflickr25k-fall.mat')['FAll']
conn = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='images')
cur = conn.cursor()
pattern = re.compile('im(.*?).jpg',re.S)

for i in range(1,file.shape[0]):
    items = re.findall(pattern, file[i][0][0])
    # print(items[0])
    # print('im{}.jpg'.format(re.findall(pattern, file[i][0][0])[0]))
    id = re.findall(pattern, file[i][0][0])[0]
    with open('Data_preprocessing/mirflickr/im{}.jpg'.format(id),'rb') as fd:
        data = fd.read()
    try:
        sql = "insert into Images values(%s,%s)"
        cur.execute(sql,[str(id),data])
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("错误信息：",e)


#
# fin = open("Data_preprocessing/mirflickr/im1.jpg",encoding='mbcs')
# img = fin.read()
# fin.close()
# cursor = conn.cursor()
# cursor.execute("INSERT INTO Images SET Data='%s'" % pymysql.escape_string(img))
# conn.commit()
# cursor.close()
# conn.close()


# with open("image/" + get_a_title + ".jpg", "rb") as f:
#     # 转为二进制格式，并且使用base64进行加密
#     base64_data = base64.b64encode(f.read())
#     a = str(i)
#     b = (j + 1)
#     c = str(b)
#     # MySQL
#     MySQL_connect(c + "-" + a, get_a_src, get_a_title, base64_data)


