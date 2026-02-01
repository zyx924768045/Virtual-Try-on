import pymysql
# pip install pymysql 


def connect_mysql_server(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE):
    try:
        conn = pymysql.connect(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            charset="utf8"
        )
        return conn
    except:
        print("unable to connect to the database")


def close(conn):
    if conn:
        conn.close()


def search_in_mysql(conn, result):
    cur = conn.cursor()
    sql = "select * from imgae_info where id in (" + str(result) + ");"
    # print(sql)
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except:
        print("search faild!")
    finally:
        cur.close()


def execute_sql(conn, sql):
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print("Error: unable to fecth data: %s ,%s" % (repr(e), sql))
    finally:
        cursor.close()
    return results


def execute_del(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("delete from image_info")
    except Exception as e:
        pass
    finally:
        cursor.close()


def execute_insert(conn, image_data):
    cursor = conn.cursor()
    # sql语句
    sql = "insert into image_info(id,image) values (%s,%s)"
    # 参数化方式传参
    count = 0
    for t in image_data:
        _id, image = t
        try:
            count = count + 1
            cursor.execute(sql, [str(_id), image])
            if count % 1000 == 0:
                print('commit......count={}'.format(count))
                conn.commit()
        except Exception as e:
            print(t, e)
            pass
    # 统一提交
    conn.commit()
    # 关闭游标　
    cursor.close()
    # 关闭连接
    conn.close()


def read_data(file_dir):
    data = []
    with open(file_dir, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if line:
                data.append(line)
    return data
