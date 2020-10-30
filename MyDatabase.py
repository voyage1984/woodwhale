import pymssql

class DBModel:
    def __init__(self,name,pswd):
        print('初始化数据库模型...')
        return self.conn(name,pswd)

    def conn(self,name,pswd):
        print('开始连接...')
        try:
            self.connect = pymssql.connect('.',user = name,password= pswd, database='PyQt_db') #服务器名,账户,密码,数据库名
        except:
            print('错误！')
            return False
        if self.connect:
            print("连接成功!")
        else:
            print('连接失败!')
            return False

    def show_data(self):
        print('开始读取数据库...')
        cursor = self.connect.cursor()
        if cursor == False:
            print('打开数据库失败，无法操作！')
            return False
        else:
            print('打开数据库成功！')
        cursor.execute('select * from userlist')
        row = cursor.fetchone()
        while row:
            print(row[0],row[1],row[2])
            row = cursor.fetchone()

#
# if __name__ == '__main__':
#     conn = conn()
#     cursor = conn.cursor()
#     cursor.execute("insert into userlist(id,name,age) values (4,'n',23)")
#     conn.commit()
#     print('读取数据...')
#     cursor.execute("select * from userlist")
#     row = cursor.fetchone()
#     while row:
#         print(row[0],row[1],row[2])
#         row = cursor.fetchone()
#     conn.close()
