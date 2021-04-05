"""
    * 严格搜索与模糊搜索
    * 重新刷新输出内容
    * 自定义格式化输出
"""

from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QButtonGroup, \
    QRadioButton, QStackedLayout, QListView
from ui.history_pages.history_search_result import history_search_result

import time

class history_search(QWidget):
    def __init__(self):
        super().__init__()
        self.db = None
        self.init()

    def init(self):
        self.menus = QComboBox()
        self.menus.setView(QListView())
        self.menus.setStyleSheet("QComboBox QAbstractItemView::item {min-height: 25px;}")
        self.menus.addItem("日期")
        self.menus.addItem("标题")
        self.menus.addItem("内容")
        self.menus.setFixedSize(100,40)

        self.select_mode = QButtonGroup()
        self.select_mode_strict = QRadioButton('严格搜索')
        self.select_mode_blurry = QRadioButton('模糊搜索')
        self.select_mode.addButton(self.select_mode_strict)
        self.select_mode.addButton(self.select_mode_blurry)
        self.select_mode_strict.setChecked(True)

        self.input_search = QLineEdit()
        self.btn_search_keyword = QPushButton("搜索")
        self.btn_clear_all = QPushButton("Clear")


        self.btn_clear_all.clicked.connect(self.clear_all)
        self.btn_search_keyword.clicked.connect(self.load_keyword_info)

        self.infos = QFrame()
        self.qsl = QStackedLayout(self.infos)

        self.search_result = history_search_result()
        self.qsl.addWidget(self.search_result)

        menubar = QHBoxLayout()
        menubar.addWidget(self.menus)
        menubar.addWidget(self.input_search)
        menubar.addWidget(self.btn_search_keyword)
        menubar.addWidget(self.btn_clear_all)
        menubar.addWidget(self.select_mode_strict)
        menubar.addWidget(self.select_mode_blurry)

        layout = QVBoxLayout()
        layout.addLayout(menubar)
        layout.addWidget(self.infos)

        self.setLayout(layout)

    def set_db(self,db):
        self.db = db
        self.search_result.set_db(db)

    def load_keyword_info(self):
        index = self.get_index()
        if index == -1:
            return
        keyword = self.input_search.text()
        if self.select_mode_strict.isChecked():
            mode = 1
            print('搜索模式: 严格搜索')
        else:
            mode = 0
            print('搜索模式: 模糊搜索')
        self.search_result.show_data(index,keyword,mode)

    def get_index(self):
        index = self.menus.currentIndex()
        if (index == 0):
            print('搜索条件: 日期')
        elif index == 1:
            print('搜索条件: 标题')
        elif index == 2:
            print('搜索条件: 正文')
        else:
            index = -1
            print('错误的索引：', index)
        return index

    def clear_all(self):
        self.search_result.clear_data()



