import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='Q&A')
cursor = conn.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
# 使用预处理语句创建表
sql = """CREATE TABLE qa1 (
        ID  INT,
        QUESTION  TEXT,
        ANSWER  TEXT)"""
try:
    cursor.execute(sql)
   # 提交到数据库执行
    conn.commit()
    print('创建成功')
except:
    print('创建失败')

sql1 = '''INSERT INTO qa1(ID,QUESTION,ANSWER)
            values('1','1','1')'''
cursor.execute(sql1)
conn.commit()
cursor.close()
conn.close()