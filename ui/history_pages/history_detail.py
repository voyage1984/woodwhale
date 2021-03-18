from PyQt5.QtWidgets import QVBoxLayout,QLineEdit,QDialog,QTextEdit,QPushButton,QHBoxLayout,QLabel

import System
from PyQt5.QtCore import pyqtSignal

class history_detail(QDialog):
        _signal = pyqtSignal()
        def __init__(self):
            super().__init__()
            self.db = None
            self.init()

        def init(self):
            self.setFixedSize(500, 400)
            self.setume = QLabel('编辑')
            self.status = QLabel('编辑中')
            self.labels = QHBoxLayout()
            self.labels.addWidget(self.setume)
            self.labels.addWidget(self.status)
            self.title = QLineEdit()
            self.title.setFixedSize(400,30)
            self.article = QTextEdit()
            self.buttons = QHBoxLayout()
            self.confirm = QPushButton('保存')
            self.delete = QPushButton('删除')
            self.buttons.addWidget(self.confirm)
            self.buttons.addWidget(self.delete)
            self.layout = QVBoxLayout()
            self.layout.addLayout(self.labels)
            self.layout.addWidget(self.title)
            self.layout.addWidget(self.article)
            self.layout.addLayout(self.buttons)
            self.setLayout(self.layout)
            self.click_event()

        def set_content(self,date,title,article):
            self.status.setText('编辑中')
            self.date = date
            self.setWindowTitle(date)
            self.title.setText(title)
            self.article.setText(article)

        def click_event(self):
            self.confirm.clicked.connect(self.save_event)
            self.delete.clicked.connect(self.delete_event)

        def save_event(self):
            print('开始保存',System.func_name())
            title = self.title.text()
            article = self.article.toPlainText()
            print(title,article)
            try:
                self.db.update_tdta("history",self.date,title,article)
                self.status.setText('已保存')
                self.close()
            except:
                print('错误')

        def delete_event(self):
            print('删除事件')
            if System.dialog(self,'警告','确认删除？'):
                print('确认删除')
                if self.db.delete_data('history',"date",self.date) == True:
                    print('已删除数据：',self.date)
                    self.close()
                    self._signal.emit()
                else:
                    System.dialog(self,'删除失败！','请稍后再试')
                    print('删除失败')
            else:
                print('取消删除')



        def set_db(self,db):
            self.db = db


