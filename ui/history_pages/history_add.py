'''
    * 添加 history_today  1
    * 添加反馈（成功、失败）  1
    * label输出文字对齐
'''

from PyQt5.QtWidgets import QLabel,QWidget,QHBoxLayout,QLineEdit,QTextEdit,QVBoxLayout,QPushButton,QMessageBox
from PyQt5.QtCore import QThread,pyqtSignal

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
        self.alert = alert_thread()
        self.alert.message.connect(self.set_alert)

        self.label_alert_status = QLabel("")
        self.label_alert_detail = QLabel("")

        label_date = QLabel('date: ')
        label_title = QLabel('title: ')
        label_article = QLabel('article: ')

        label_date.setFixedSize(100,40)
        label_title.setFixedSize(100,40)
        label_article.setFixedSize(100,40)

        self.label_alert_status.setFixedSize(100,50)
        self.label_alert_detail.setFixedSize(400,50)
        # self.label_alert_status.alignment()

        self.input_date = QLineEdit()
        self.input_title = QLineEdit()
        self.input_article = QTextEdit()
        self.submit_button = QPushButton('插入')
        self.submit_button.clicked.connect(self.submit_event)

        layout_date = QHBoxLayout()
        layout_title = QHBoxLayout()
        layout_article = QHBoxLayout()
        layout_alert = QHBoxLayout()
        
        layout_date.addWidget(label_date)
        layout_date.addWidget(self.input_date)
        layout_title.addWidget(label_title)
        layout_title.addWidget(self.input_title)
        layout_article.addWidget(label_article)
        layout_article.addWidget(self.input_article)
        layout_alert.addWidget(self.label_alert_status)
        layout_alert.addWidget(self.label_alert_detail)

        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_date)
        self.layout.addLayout(layout_title)
        self.layout.addLayout(layout_article)
        self.layout.addWidget(self.submit_button)
        self.layout.addLayout(layout_alert)
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
        if  check != False:
            if check == 1:
                print('错误: 存在空值')
            elif check ==2:
                print('错误: 日期已存在')
                if self.alter_Event():
                    self.db.update_history(date,title,article)
                    self.clear_text()
                    print('更新成功')
                    self.add_alert(1)
                    self.label_alert_detail.setText('更新成功！')
            return
        else:
            if self.db.insert_history(date,title,article) == True:
                print('添加成功！')
                self.add_alert(1)
                self.label_alert_detail.setText(date)
                self.clear_text()
            else:
                self.add_alert(0)
                print('添加失败！',System.func_name())
                self.show_err()

    def check_history(self,date,title,artile):
        err_msg = "add_history.check_history"
        result = 1
        if len(date)==0 or len(title)==0 or len(artile)==0:
            print('不能输入空值！: ',err_msg)
            self.label_alert_detail.setText("存在空值！")
        elif self.check_exist(date):
            print('该日期已存在！')
            self.label_alert_detail.setText("日期已存在！")
            result = 2
        else:
            result = False
        self.add_alert(0)
        return result

    def check_exist(self,date):
        print('检查日期: ',date,"是否存在...")
        search = self.db.get_search_from_table(0,date,'history',1)
        if len(search) == 0:
            print('未查询到数据: ',date)
            return False
        else:
            print('已查询该数据: ',date)
            return True


    def clear_text(self):
        self.input_date.setText("")
        self.input_title.setText("")
        self.input_article.setText("")

    def add_alert(self,status):
        self.alert.show_alert(status)

    def set_alert(self,message):
        print('设置状态: ',message)
        self.label_alert_status.setText(message)

    def alter_Event(self):
        print('修改事件: history_add.alter_Event')
        reply = QMessageBox.question(self, '内容已存在',
                                     "是否更新?",QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print('确认更新',System.func_name())
            return True
        else:
            print('取消更新',System.func_name())
            return False

    def show_err(self):
        reply = QMessageBox.question(self, '插入失败！',
                                     "请检查输入", QMessageBox.Yes |
                                     QMessageBox.No)

class alert_thread(QThread):
    success = "成功！"
    failed  = "失败！"

    message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.sec = 3000

    def show_alert(self,status):
        if status == 0:
            self.message.emit(self.failed)
        else:
            self.message.emit(self.success)







