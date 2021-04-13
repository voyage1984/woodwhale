from PyQt5.QtWidgets import QLabel,QWidget,QHBoxLayout,QLineEdit,QTextEdit,QVBoxLayout,QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt

import MyDatabase
import System

class history_add(QWidget):
    def __init__(self):
        self.db = MyDatabase.DBModel()
        super().__init__()
        self.init()

    def set_db(self,db):
        self.db = db

    def init(self):
        label_date = QLabel('date: ')
        label_title = QLabel('title: ')
        label_article = QLabel('article: ')

        label_date.setFixedSize(100,40)
        label_title.setFixedSize(100,40)
        label_article.setFixedSize(100,40)


        self.input_date = QLineEdit()
        self.input_title = QLineEdit()
        self.input_article = QTextEdit()
        self.submit_button = QPushButton('插入')
        self.submit_button.clicked.connect(self.submit_event)

        layout_date = QHBoxLayout()
        layout_title = QHBoxLayout()
        layout_article = QHBoxLayout()
        
        layout_date.addWidget(label_date)
        layout_date.addWidget(self.input_date)
        layout_title.addWidget(label_title)
        layout_title.addWidget(self.input_title)
        layout_article_v = QVBoxLayout()
        layout_article_v.setAlignment(Qt.AlignTop)
        layout_article_v.addWidget(label_article)
        layout_article.addLayout(layout_article_v)
        layout_article.addWidget(self.input_article)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_date)
        self.layout.addLayout(layout_title)
        self.layout.addLayout(layout_article)
        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

    def submit_event(self):
        if self.db.status(0) != False:
            self.insert_data()
        else:
            print('连结数据库错误!',System.func_name())

    def insert_data(self):
        print('开始插入数据',System.func_name())
        date = self.input_date.text()
        title = self.input_title.text()
        article = self.input_article.toPlainText()
        check = self.check_history(date,title,article)
        if check == "empty":
            print('错误: 存在空值')
            System.dialog(self,'错误','存在空值')
            return
        elif check == "error":
            System.dialog(self, '错误', '获取内容错误！')
            return
        elif check == "none":
            print("即将插入数据")
            if self.db.insert_tdta("history",date,title,article) == True:
                print('添加成功！')
                self.clear_text()
            else:
                print('添加失败！',System.func_name())
                self.show_err()
        else:
            print('错误: 日期已存在'+date[4:8])
            if self.alter_Event():
                self.db.update_table("history","date",date,"date",str(check))
                if(self.db.update_tdta("history",date,title,article)):
                    self.clear_text()
                    print('更新成功')
                else:
                    System.dialog(self,"更新失败！","请联系管理员")
                    return
        return


    def check_history(self,date,title,artile):
        if len(date)==0 or len(title)==0 or len(artile)==0:
            print('不能输入空值！',System.func_name())
            return "empty"
        else:
            return self.check_exist(date)

    def check_exist(self,date):
        """19990101 1999-01-01"""
        if(len(date)==8):
            str = "-"+date[4:6]+"-"+date[6:8]
        elif(len(date)==10):
            str = date[4:9]
        else:
            print("获取内容错误：",date)
            return "error"
        print('检查日期: ',str,"是否存在...")
        search = self.db.get_search_from_table(0,str,'history',0)
        if len(search) == 0:
            print('未查询到数据: ',date)
            return "none"
        else:
            print('已查询该数据: ',date)
            return search[0][0]


    def clear_text(self):
        self.input_date.setText("")
        self.input_title.setText("")
        self.input_article.setText("")

    def alter_Event(self):
        print('修改事件: history_add.alter_Event')
        if System.dialog(self,'内容已存在',"是否更新?",):
            print('确认更新',System.func_name())
            return True
        else:
            print('取消更新',System.func_name())
            return False

    def show_err(self):
        System.dialog(self,'插入失败！',"请检查输入")






