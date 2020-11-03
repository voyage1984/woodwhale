import pymssql

class DBModel:
    def __init__(self):
        print('初始化数据库模型...')
        self.myconnect = None

    def conn(self,name,pswd):
        print('开始连接数据库...')
        try:
            self.myconnect = pymssql.connect('.',user = name,password= pswd, database='PyQt_db') #服务器名,账户,密码,数据库名
        except:
            print('连接数据库错误！: MyDatabase.DBModel.conn')
            return False
        if self.myconnect:
            print("连接数据库成功!")
        else:
            print('连接数据库失败!: MyDatabase.DBModel.conn')
            return False
        return True

    def show_data(self):
        print('开始读取数据库...')
        cursor = None
        try:
            cursor = self.myconnect.cursor()
        except:
            print('打开数据库失败！: MyDatabase.DBModel.show_data[1]')
        if cursor == False:
            print('打开数据库失败！: MyDatabase.DBModel.show_data [2]')
            return False
        else:
            print('打开数据库成功！')
        cursor.execute('select * from userlist')
        row = cursor.fetchone()
        result = []
        while row:
            result.append(row[0])
            result.append(row[1])
            result.append(row[2])
            row = cursor.fetchone()
        return result

    def status(self):
        try:
            cursor = self.myconnect.cursor()
        except:
            print('未连接数据库: MyDatabase.DBModel.status [1]')
            return False
        if cursor == False:
            print('未连接数据库: MyDatabase.DBModel.status [2]')
            return False
        else:
            print('已连接数据库: MyDatabase.DBModel.status [3]')
            return True

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
