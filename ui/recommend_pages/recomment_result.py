from PyQt5.QtWidgets import QWidget,QHBoxLayout,QLabel,QListWidget,QGridLayout
from PyQt5.QtWidgets import QApplication

import System

class recommend_result(QWidget):
    def __init__(self):
        super().__init__()
        self.db = None
        self.init()

    def set_db(self,db):
        self.db = db

    def init(self):
        self.list = QListWidget()
        self.list.addItem("-----结果-----")
        self.layout = QGridLayout()
        self.layout.addWidget(self.list,0,0,10,8)
        self.setLayout(self.layout)

    def get_data(self):
        if self.db == None:
            print('数据库初始化失败！',System.func_name())
            return
        list = self.db.get_all_from_table('recommend')
        if len(list) == 0:
            print('没有数据',System.func_name())
            self.list.addItem('没有数据！')
            return
        for line in list:
            print(line[1].encode('latin-1', errors='ignore').decode('gbk', errors='ignore'))
            data = str(line[0]).strip()
            title = str(line[1].encode('latin-1').decode('gbk')).strip()
            article = str(line[2].encode('latin-1').decode('gbk')).strip()
            string = data + '\t' + title + '\t' + article
            self.list.addItem(string)
        QApplication.processEvents()
        print('显示完成')

