import pymssql

E_get_user = 0
E_show_data = 1


class DBModel:
    def __init__(self):
        # print('初始化数据库模型: MyDatabase.DBModel.__init__')
        self.myconnect = None
        self.history_table = ['dateday','title','article']

    def conn(self,name,pswd):
        print('开始连接数据库: MyDatabase.DBModel.conn')
        try:
            self.myconnect = pymssql.connect('.',user = name,password= pswd, database='PyQt_db') #服务器名,账户,密码,数据库名
        except:
            print('连接数据库错误！: MyDatabase.DBModel.conn[1]')
            return False
        if self.myconnect:
            print("连接数据库成功!: MyDatabase.DBModel.conn")
        else:
            print('连接数据库失败!: MyDatabase.DBModel.conn[2]')
            return False
        return True

    def show_data(self,cmd):
        print('开始读取数据库: MyDatabase.DBModel.show_data')
        cursor = None
        try:
            cursor = self.myconnect.cursor()
        except:
            print('打开数据库失败！: MyDatabase.DBModel.show_data[1]')
        if cursor == False:
            print('打开数据库失败！: MyDatabase.DBModel.show_data [2]')
            return False
        else:
            print('打开数据库成功！: MyDatabase.DBModel.show_data')
        sqlcmd = 'select * from '+str(cmd)
        print('执行sql语句: ',sqlcmd)
        cursor.execute(sqlcmd)
        row = cursor.fetchone()
        result = []
        while row:
            result.append(row[0])
            result.append(row[1])
            result.append(row[2])
            result.append('\n')
            row = cursor.fetchone()
        return result

    def get_user(self):
        print('开始获取当前用户: MyDatabase.DBModel.get_user')
        cursor = self.status(E_get_user)
        if cursor == False:
            return False
        cursor.execute('select SYSTEM_USER')
        r = cursor.fetchone()
        return r

    def status(self,err_n):
        try:
            cursor = self.myconnect.cursor()
        except:
            print('未连接数据库: MyDatabase.DBModel.status [1]: ',err_n)
            return False
        if cursor == False:
            print('未连接数据库: MyDatabase.DBModel.status [2]',err_n)
            return False
        else:
            print('已连接数据库：MyDatavase.DBModel.status')
            return cursor

    def get_colName(self,col,table):
        if len(self.history_table) < col:
            print('未知的列名: ',col,table)
            return -1
        return self.history_table[col]

    def insert_history(self,date,title,article):
        cursor = self.status(0)
        if cursor != False:
            sqlcmd = "insert into history(dateday,title,article) values('"+date+"','"+title+"','"+article+"')"
            print("执行sql语句：",sqlcmd)
            try:
                cursor.execute(sqlcmd)
                self.myconnect.commit()
                return True
            except pymssql.Error:
                print("执行语句失败！")
                return False
        else:
            print('连接数据库失败: MyDatabase.DBMode.insert_history')
            return False

    def update_history(self,date,title,article):
        cursor = self.status(0)
        if cursor != False:
            sqlcmd_title = "update history set title='" + title + "' where dateday = '" + date + "'"
            sqlcmd_article = "update history set article='" + article + "' where dateday = '" + date + "'"
            print("执行sql语句：", sqlcmd_title)
            print("执行sql语句：", sqlcmd_article)
            try:
                cursor.execute(sqlcmd_title)
                cursor.execute(sqlcmd_article)
                self.myconnect.commit()
                return True
            except pymssql.Error:
                print("执行语句失败！")
                return False
        else:
            print('连接数据库失败: MyDatabase.DBMode.insert_history')
            return False

    def get_all_from_table(self,table):
        print('查询数据表: ',table)
        cursor = self.status(0)
        if cursor != False:
            sqlcmd = "select * from "+table
            print("执行sql语句：",sqlcmd)
            cursor.execute(sqlcmd)
            list = cursor.fetchall()
            # self.myconnect.commit()
            print("查询成功！\n")
            return list
        else:
            print("查询失败！：MyDatabase.DBModel.get_all")
            return False

    def get_search_from_table(self,col,keyword,table,mode):
        cursor = self.status(0)
        if cursor != False:
            print('开始读取数据表: ',table)
            colname = self.get_colName(col,table)
            if colname == -1:
                print('获取列名失败！: MyDatabase.DBModel.get_search_from_table()')
                return
            print('获取列名成功: ',colname)
            if mode == 1:
                print('搜索模式: 严格搜索')
                sqlcmd = "select * from " + table + ' where ' + colname + " = '" + keyword+"'"
            else:
                print('搜索模式: 模糊搜索')
                sqlcmd = "select * from " + table + ' where ' + colname + " like '%" + keyword + "%'"
            try:
                print("执行sql语句：", sqlcmd)
                cursor.execute(sqlcmd)
                print('开始获取数据...')
                list = cursor.fetchall()
                return list
            except:
                print('发生了错误！: MyDatabase.get_search_from_table')
                return ""
        else:
            print("查询失败！：MyDatabase.DBModel.get_all")
            return False
