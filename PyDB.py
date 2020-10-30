"""
    弃用方案pymysql: MySql，改用pymssql：SQL Server
    见：MyDatabase.py
"""

# 此文件已弃用
# import pymysql
#
# class MyDB:
#     def __init__(self):
#         print('初始化数据库...')
#
#
#     def connect(self,name,password):
#         print('连接数据库...')
#         conn = pymysql.connect(
#             host="Localhost",
#             user = name,
#             password = password,
#             database = "PyQt_db",
#             charset = 'utf-8'
#         )
#         return conn
#
#     def showtable(self,name,password):
#         conn = self.connect(name,password)
#         cursor = conn.cursor()
#         cursor.execute("select * from list")
#         for i in cursor.next():
#             print(i)
#
#     def create_db(self):
#         print('创建数据库...')
#         conn = self.connect('username','password')
#         sql = "CREATE DATABASE IF NOT EXISTS MyDB.db"
#         print('开始创建！。。。')
#
#         cursor = conn.cursor()
#         try:
#             print('正在创建！。。。')
#             cursor.execute(sql)
#         except:
#             print('创建数据库失败')
#             return
#         print('创建数据库成功！')
#         sql2 = '''create table 'mylist'(
#             'id' INT NOT NULL AUTO_INCREMENT,
#             'name' CHAR(10) NOT NULL,
#             'age' INT NOT NULL,
#             PRIMARY KEY('id')
#         )'''
#         try:
#             print('创建数据表...')
#             cursor.execute(sql2)
#         except:
#             print("创建数据表失败！")
#             return
#         sql3 = '''insert into 'mylist'(name,age)
#             values('bob',1);
#         '''
#         try:
#             print('添加数据...')
#             cursor.execute(sql3)
#         except:
#             print("添加数据失败！")
#             return