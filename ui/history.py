from PyQt5.QtWidgets import QWidget,QLabel,QVBoxLayout,QHBoxLayout,QPushButton,QFrame,QStackedLayout

from ui.history_pages import history_search
from ui.history_pages import history_add
from MyDatabase import DBModel

class history(QWidget):
    def __init__(self):
        self.db = DBModel()
        self.db = None
        super().__init__()
        self.init()

    def init(self):
        self.btn_search = QPushButton("查询记录")
        self.btn_addnew = QPushButton("新建")
        self.btn_search.setFixedSize(100,40)
        self.btn_addnew.setFixedSize(100,40)

        frame = QFrame()
        self.qsl = QStackedLayout(frame)

        self.search_page = history_search.history_search()
        self.add_page = history_add.history_add()
        self.qsl.addWidget(self.search_page)
        self.qsl.addWidget(self.add_page)

        leftside = QVBoxLayout()
        leftside.addWidget(self.btn_search)
        leftside.addWidget(self.btn_addnew)

        layout = QHBoxLayout()
        layout.addLayout(leftside)
        layout.addWidget(frame)

        self.click_event()

        self.setLayout(layout)

    def click_event(self):
        self.btn_search.clicked.connect(lambda :self.to_page(0))
        self.btn_addnew.clicked.connect(lambda :self.to_page(1))

    def set_db(self,db):
        self.db = db
        self.search_page.set_db(db)
        self.add_page.set_db(db)

    def to_page(self,num):
        self.qsl.setCurrentIndex(num)
