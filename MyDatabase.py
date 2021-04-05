import pymssql
import System

E_get_user = 0
E_show_data = 1


class DBModel:
    def __init__(self):
        self.myconnect = None
        self.col_name= System.col_name

    def conn(self,name,pswd):
        print('开始连接数据库',System.func_name())
        try:
            print(name,pswd,System.db_name)
            self.myconnect = pymssql.connect('.',user = name,password= pswd, database=System.db_name) #服务器名,账户,密码,数据库名
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
        if table=='booklist':
            print('获取booklist的列名')
            return self.col_name[1][col]
        elif table=="userlist":
            return col
        else:
            print('获取'+table+'的列名')
            return self.col_name[0][col]

    def insert_tdta(self,table,date,title,article):
        cursor = self.status(0)
        print('开始执行insert命令')
        if cursor != False:
            print('获取游标成功！',System.func_name())
            if (date==None):
                sqlcmd = "insert into "+table+" (title, article) values('"+title+"','"+article+"')"
            else:
                sqlcmd = "insert into "+table+" (date, title, article) values('"+str(date)+"','"+title+"','"+article+"')"
            print("执行sql语句：", sqlcmd)
            try:
                cursor.execute(sqlcmd)
                print('开始提交...')
                self.myconnect.commit()
                return True
            except Exception as err:
                print("执行语句失败！", System.func_name())
                print(err)
                return False
        else:
           print('连接数据库失败', System.func_name())
        return False

    def update_tdta(self,table,date,title,article):
        cursor = self.status(0)
        if cursor != False:
            sqlcmd_title = "update "+table+" set title "+ "= '"+ title + "' where date = '" + date + "'"
            sqlcmd_article = "update "+table+" set article = '" + article + "' where date = '" + date + "'"
            print("执行sql语句：", sqlcmd_title)
            print("执行sql语句：", sqlcmd_article)
            try:
                cursor.execute(sqlcmd_title)
                cursor.execute(sqlcmd_article)
                self.myconnect.commit()
                print('修改数据成功',System.func_name())
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
                list = cursor.fetchall()
                print('获取数据成功！')
                return list
            except:
                print('发生了错误！',System.func_name())
                return ""
        else:
            print("查询失败！",System.func_name())
            return False

    def update_table(self,table,colName,colValue,cdt,cdtName):
        cursor = self.status(0)
        sqlcmd = ''
        if cursor != False:
            print('开始读取数据表: ',table)
            sqlcmd = "update " + table + ' set ' + colName + " = '" + colValue+"' where "+cdt+"= '"+cdtName+"'"
            print("执行sql语句：", sqlcmd)
        try:
            cursor.execute(sqlcmd)
            self.myconnect.commit()
            print('更新数据成功！')
            return True
        except:
            print('发生了错误！',System.func_name())
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
            except pymssql.Error:
                print('执行失败！',System.func_name())
        else:
            print("删除失败！",System.func_name())
        return False

    def update_book(self,table,id,title,author,company,publish):
        cursor = self.status(0)
        if cursor != False:
            sqlcmd_title = "update "+table+" set title = '"+ title + "' where id = " + id
            sqlcmd_author = "update "+table+" set author = '" + author + "' where id = " + id
            sqlcmd_company = "update "+table+" set company = '" + company + "' where id = " + id
            sqlcmd_publish = "update "+table+" set publish = '" + publish + "' where id = " + id
            print("执行sql语句：",sqlcmd_title)
            try:
                cursor.execute(sqlcmd_title)
                cursor.execute(sqlcmd_author)
                cursor.execute(sqlcmd_company)
                cursor.execute(sqlcmd_publish)
                self.myconnect.commit()
                print('修改数据成功',System.func_name())
                return True
            except pymssql.Error:
                print("执行语句失败！",System.func_name())
                return False
        else:
            print('连接数据库失败',System.func_name())
            return False

    def insert_book(self,list):
        cursor = self.status(0)
        print('开始执行insert命令')
        if cursor != False:
            print('获取游标成功！', System.func_name())
            sqlcmd = "insert into booklist (title, author,company,publish,total,rest,booknum,tag1,tag2) values('"
            sqlcmd += list[0]+"','"+list[1]+"','"+list[2]+"','"+list[3]+"',"+list[4]+","+list[4]+",'"
            sqlcmd += list[5]+"','"+list[6]+"','"+list[7]+"')"
            print("执行sql语句：", sqlcmd)
            try:
                cursor.execute(sqlcmd)
                print('开始提交...')
                self.myconnect.commit()
                return True
            except Exception as err:
                print("执行语句失败！", System.func_name())
                print(err)
                return False
        else:
            print('连接数据库失败', System.func_name())
        return False
        return True
