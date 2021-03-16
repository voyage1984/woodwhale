import pymssql
import System

E_get_user = 0
E_show_data = 1


class DBModel:
    def __init__(self):
        # print('初始化数据库模型: MyDatabase.DBModel.__init__')
        self.myconnect = None
        self.history_table = System.l_history

    def conn(self,name,pswd):
        print('开始连接数据库',System.func_name())
        try:
            print(name,pswd,System.db_name)
            self.myconnect = pymssql.connect('.',user = name,password= pswd, database=System.db_name,charset="utf8") #服务器名,账户,密码,数据库名
        except Exception as e:
            print(e)
            print('连接数据库错误！',System.func_name())
            print('登录ID：',name,"\t登录密码：",pswd)
            return False
        if self.myconnect:
            print("连接数据库成功!",System.func_name())
        else:
            print('连接数据库失败!',System.func_name())
            return False
        return True

    def show_data(self,cmd):
        print('开始读取数据库',System.func_name())
        cursor = None
        try:
            cursor = self.myconnect.cursor()
        except:
            print('打开数据库失败！',System.func_name())
        if cursor == False:
            print('获取游标失败！',System.func_name())
            return False
        else:
            print('获取游标成功！')
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
        print('开始获取当前用户',System.func_name())
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
            print('未连接数据库: ',err_n,System.func_name())
            return False
        if cursor == False:
            print('获取游标失败: ',err_n,System.func_name())
            return False
        else:
            print('已连接数据库',System.func_name())
            return cursor

    def get_colName(self,col,table):
        if len(self.history_table) < col:
            print('未知的列名: ',col,table)
            return -1
        return self.history_table[col]

    def insert_history(self,date,title,article):
        cursor = self.status(0)
        if cursor != False:
            sqlcmd = "insert into history("+self.history_table[0]+","+self.history_table[1]+","+self.history_table[2]+") values('"+date+"','"+title+"','"+article+"')"
            print("执行sql语句：",sqlcmd)
            try:
                """
                提交非法数据后再提交合法数据有BUG 
                """
                cursor.execute(sqlcmd)
                print('开始提交...')
                self.myconnect.commit()
                return True
            except Exception as err:
                print("执行语句失败！",System.func_name())
                print(err)
                return False
        else:
            print('连接数据库失败',System.func_name())
            return False

    def update_history(self,date,title,article):
        cursor = self.status(0)
        if cursor != False:
            sqlcmd_title = "update history set " +self.history_table[1] +" ='" + title + "' where "+ self.history_table[0] +" = '" + date + "'"
            sqlcmd_article = "update history set "+self.history_table[2] +" = '" + article + "' where " +self.history_table[0]+" = '" + date + "'"
            print("执行sql语句：", sqlcmd_title)
            print("执行sql语句：", sqlcmd_article)
            try:
                cursor.execute(sqlcmd_title)
                cursor.execute(sqlcmd_article)
                self.myconnect.commit()
                return True
            except pymssql.Error:
                print("执行语句失败！",System.func_name())
                return False
        else:
            print('连接数据库失败',System.func_name())
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
            print("查询成功！",System.func_name())
            return list
        else:
            print("查询失败！",System.func_name())
            return False

    def get_search_from_table(self,col,keyword,table,mode):
        cursor = self.status(0)
        if cursor != False:
            print('开始读取数据表: ',table)
            colname = self.get_colName(col,table)
            if colname == -1:
                print('获取列名失败！',System.func_name())
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
                print('发生了错误！',System.func_name())
                return ""
        else:
            print("查询失败！",System.func_name())
            return False

    def delete_data(self,table,keyword,value):
        print("执行删除",System.func_name())
        cursor = self.status(0)
        if cursor != False:
            sqlcmd = "delete from "+table+" where "+ keyword + " = "+ "'"+value+"'"
            try:
                print("执行sql命令: ",sqlcmd)
                cursor.execute(sqlcmd)
                self.myconnect.commit()
                print('删除成功！')
                return True
            except:
                print('执行失败！',System.func_name())
        else:
            print("删除失败！",System.func_name())
        return False

