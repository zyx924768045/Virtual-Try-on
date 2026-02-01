import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='q&a')

def insert(tt):
    cursor = conn.cursor()
    sql22 = "select * from qa1 where id = (select max(id) from qa1);"
    t = cursor.execute(sql22)
    # 获取所有记录列表
    results = cursor.fetchall()
    count2 = results[0][0]
    print(count2)
    #print(count2)
    #print(tt)
    sql111 = '''INSERT INTO qa1(ID,QUESTION,ANSWER)
            values('%s','%s','%s')'''
    count2 = count2 + 1
    print(count2, tt[0], tt[1],)
    cursor.execute(sql111 % (count2, tt[0], tt[1]))
    conn.commit()
    #print('写入数据库失败')
    cursor.close()
    #conn.close()

def countjdd():
    cursor = conn.cursor()
    sql22 = "select * from qa1 where id = (select max(id) from qa1);"
    t = cursor.execute(sql22)
    # 获取所有记录列表
    results = cursor.fetchall()
    count2 = results[0][0]
    cursor.close()
    #conn.close()
    return count2
