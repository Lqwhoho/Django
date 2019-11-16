import pymysql.cursors


conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='admin123456',
                       db='event_manage',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursors:  # 创建嘉宾表
        sql = 'INSERT INTO  sign_guest(realname, phone, email, sign, id, create_time) VALUE ("lisa", "13567890987",' \
              ' "lisa@mail.com", 0, 2, NOW())'
        cursors.execute(sql)
        conn.commit()   # 提交事务

    with conn.cursor() as cursor:
        sql = "SELECT * FROM sign_guest WHERE phone=%s"
        cursor.execute(sql, '13567890987')
        result = cursor.fetchone()
        print(result)
finally:
    conn.close()
