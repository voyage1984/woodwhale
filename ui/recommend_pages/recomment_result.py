from PyQt5.QtWidgets import QWidget, QListWidget,QGridLayout
from PyQt5.QtWidgets import QApplication

import System
from ui import item_detail


class recommend_result(QWidget):
    def __init__(self):
        super().__init__()
        self.db = None
        self.init()

    def set_db(self,db):
        self.db = db
        self.detail.set_db(db,'recommend')

    def init(self):
        self.keyword = ''
        self.list = QListWidget()
        self.list.addItem("-----结果-----")
        self.layout = QGridLayout()
        self.layout.addWidget(self.list,0,0,10,8)
        self.setLayout(self.layout)
        self.list.itemClicked.connect(self.item_detail)
        self.detail = item_detail.item_detail()

    def get_data(self):
        System.clear_data(self)
        if self.db == None:
            print('数据库初始化失败！',System.func_name())
            return
        list = self.db.get_all_from_table('recommend')
        if len(list) == 0:
            print('没有数据',System.func_name())
            self.list.addItem('没有数据！')
            return
        System.set_list(self.list,list)
        QApplication.processEvents()
        print('显示完成')

    def set_data(self,keyword):
        self.keyword = keyword
        print('开始获取内容',System.func_name())
        System.clear_data(self)
        r_title = self.db.get_search_from_table(1,keyword,'recommend',0)
        System.set_list(self.list,r_title)
        QApplication.processEvents()
        print('显示完成')

    def item_detail(self):
        print('item detail',System.func_name())
        item = self.list.currentItem()
        date = System.get_item(item)[0][:-3]
        if System.is_item(date) == False:
            print('非item')
        else:
            title = System.get_item(item)[1]
            article = System.get_item(item)[2]
            print(date+'\t'+title+'\t'+article)
            self.detail._signal.connect(self.renew_item)
            self.detail.set_content(date, title, article)
            self.detail.exec()

    def renew_item(self):
        self.set_data(self.keyword)


