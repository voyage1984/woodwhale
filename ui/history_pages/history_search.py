"""
    * 严格搜索与模糊搜索
    * 重新刷新输出内容
    * 自定义格式化输出
"""

from PyQt5.QtWidgets import QWidget,QComboBox, QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QFrame,QLabel,QStackedLayout
from ui.history_pages.history_search_result import history_search_result

class history_search(QWidget):
    def __init__(self):
        super().__init__()
        self.db = None
        self.init()

    def init(self):
        self.menus = QComboBox()
        self.menus.addItem("日期")
        self.menus.addItem("标题")
        self.menus.addItem("内容")
        self.menus.setFixedSize(100,40)

        self.input_search = QLineEdit()
        self.btn_search_keyword = QPushButton("搜索")
        self.btn_search_all = QPushButton("搜索全部")

        self.btn_search_all.clicked.connect(self.load_all_info)
        self.btn_search_keyword.clicked.connect(self.load_keyword_info)

        self.infos = QFrame()
        self.qsl = QStackedLayout(self.infos)

        self.search_result = history_search_result()
        self.qsl.addWidget(self.search_result)

        menubar = QHBoxLayout()
        menubar.addWidget(self.menus)
        menubar.addWidget(self.input_search)
        menubar.addWidget(self.btn_search_keyword)
        menubar.addWidget(self.btn_search_all)

        layout = QVBoxLayout()
        layout.addLayout(menubar)
        layout.addWidget(self.infos)

        self.setLayout(layout)

    def set_db(self,db):
        self.db = db

    def load_all_info(self):
        info = self.db.get_all_from_table("history")
        self.search_result.show_data(info)

    def load_keyword_info(self):
        print('点击搜索: history_search.load_keyword_info')
        index = self.get_index()
        if index == -1:
            return
        keyword = self.input_search.text()
        print("搜索关键词: ",keyword)
        if len(keyword) == 0:
            print('请输入关键词！: history_search.load_keyword_info')
            return
        info = self.db.get_search_from_table(index,keyword,'history')
        self.search_result.show_data(info)

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




