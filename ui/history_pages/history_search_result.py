from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QLabel,QPushButton,QListWidget,QGridLayout, QMessageBox
from PyQt5.QtWidgets import QApplication

import System
from PyQt5.QtCore import pyqtSignal

from ui.history_pages import history_detail

class history_search_result(QWidget):
    def __init__(self):
        super().__init__()
        self.db = None
        self.init()

    def set_db(self,db):
        self.db = db
        self.detail.set_db(db)

    def init(self):
        self.result = ''
        self.list = QListWidget()
        self.list.addItem("-----搜索-----")
        self.layout = QGridLayout()
        self.layout.addWidget(self.list,0,0,10,8)
        self.setLayout(self.layout)
        self.list.itemClicked.connect(self.item_detail)
        self.detail = history_detail.history_detail()

    def show_data(self,result):
        self.result = result
        self.clear_data()
        print("开始显示...")
        if len(result) == 0:
            print('没有数据！')
            self.list.addItem("没有数据！")
            return
        for line in result:
            print(line[1].encode('latin-1', errors='ignore').decode('gbk', errors='ignore'))
            data = str(line[0]).strip()
            title = str(line[1].encode('latin-1').decode('gbk')).strip()
            article = str(line[2].encode('latin-1').decode('gbk')).strip()
            string = data+'\t'+title+'\t'+article
            self.list.addItem(string)
            # self.list.addLayout(self.list_view(data,title,article))
        QApplication.processEvents()
        print('显示完成')

    def list_view(self, data, title, article):
        label_data = QLabel(data)
        label_title = QLabel(title)
        label_article = QLabel(article)
        line = QHBoxLayout()
        line.addWidget(label_data)
        line.addWidget(label_title)
        line.addWidget(label_article)

        return line

    def clear_data(self):
        print('开始遍历: history_search_result.clear_data')
        count = self.list.count()
        print('遍历范围:',count)
        for i in range(count):
            self.list.takeItem(0)

    def get_item(self,item):
        result = item.text().split("\t")
        return result

    def item_detail(self):
        print('item detail')
        item = self.list.currentItem()
        date = self.get_item(item)[0]
        title = self.get_item(item)[1]
        article = self.get_item(item)[2]
        print(date)
        if self.is_item(date) == False:
            return
        self.detail._signal.connect(lambda:self.delete_item(item))
        self.detail.set_content(date,title,article)
        self.detail.exec()

    def delete_item(self,item):
        self.list.takeItem(self.list.row(item))
        print('已刷新')

    def is_item(self,date):
        try:
            result = date.replace('-','')
            print('result = ',result)
            if result.isdigit():
                print('数据对象：',date)
                return True
            else:
                print('非数据对象')
                return False
        except:
            print('发生了错误！',System.func_name())
            return False
