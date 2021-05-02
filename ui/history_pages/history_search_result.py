from PyQt5.QtWidgets import QWidget, QListWidget,QGridLayout
from PyQt5.QtWidgets import QApplication

import System

from ui import item_detail


class history_search_result(QWidget):
    def __init__(self):
        super().__init__()
        self.db = None
        self.result = None
        self.init()

    def set_db(self,db):
        self.db = db
        self.detail.set_db(db,'history')

    def init(self):
        self.index = ''
        self.keyword = ''
        self.mode = ''
        self.list = QListWidget()
        self.list.addItem("-----搜索-----")
        self.layout = QGridLayout()
        self.layout.addWidget(self.list,0,0,10,8)
        self.setLayout(self.layout)
        self.list.itemClicked.connect(self.item_detail)
        self.detail = item_detail.item_detail()

    def show_data(self,index,keyword,mode):
        self.index = index
        self.keyword = keyword
        self.mode = mode
        if len(keyword) == 0:
            print('没有关键词, 默认搜索全部')
            self.result = self.db.get_all_from_table('history')
        else:
            print("搜索关键词: ", keyword)
            self.result = self.db.get_search_from_table(index, keyword, 'history', mode)
        self.clear_data()
        print("开始显示...")
        if len(self.result) == 0:
            print('没有数据！')
            self.list.addItem("没有数据！")
            return
        System.set_list(self.list,self.result,"日期","标题","正文")
        QApplication.processEvents()
        print('显示完成')

    def clear_data(self):
        System.clear_data(self)

    def item_detail(self):
        print('item detail')
        index = self.list.currentIndex().row()
        if index == 0:
            print('非item')
            return
        else:
            print("是item")
            item = self.result[index - 1]
            id = item[0]
            print(item[1])
            title = str(item[1].encode('latin-1').decode('gbk')).strip()
            article = str(item[2].encode('latin-1').decode('gbk')).strip()
        # print(date)
        self.detail._signal.connect(self.renew_item)
        self.detail.set_content(str(id),title,article)
        self.detail.exec()

    def renew_item(self):
        self.show_data(self.index,self.keyword,self.mode)
        print('已刷新')

