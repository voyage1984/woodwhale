from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QFrame,QStackedLayout

from ui.history import history
from ui.recommend import recommend
from MyDatabase import DBModel

class tools(QWidget):
    tool_list = ['推荐','历史','tip','公告']

    def __init__(self):
        self.db = DBModel()
        super().__init__()
        self.init()

    def init(self):
        self.btn_recommend = QPushButton("推荐")
        self.btn_history = QPushButton("历史上的今天")
        self.btn_tip = QPushButton("小tip")
        self.btn_announce = QPushButton("公告")
        self.btn_tip.setFixedSize(250,35)
        self.btn_history.setFixedSize(250,35)
        self.btn_announce.setFixedSize(250,35)
        self.btn_recommend.setFixedSize(250,35)

        frame = QFrame(self)

        self.qsl = QStackedLayout(frame)

        toolbar = QHBoxLayout()
        layout = QVBoxLayout()

        toolbar.addWidget(self.btn_recommend)
        toolbar.addWidget(self.btn_history)
        toolbar.addWidget(self.btn_tip)
        toolbar.addWidget(self.btn_announce)

        self.loadPages()
        self.btn_event()

        layout.addLayout(toolbar)
        layout.addWidget(frame)

        self.setLayout(layout)

    def loadPages(self):
        self.history_page = history()
        self.recommend_page = recommend("recommend")
        self.tip_page = recommend("tips")
        self.annouce_page = recommend("annouce")

        self.qsl.addWidget(self.recommend_page)
        self.qsl.addWidget(self.history_page)
        self.qsl.addWidget(self.tip_page)
        self.qsl.addWidget(self.annouce_page)

    def setdb(self,db):
        self.db = db
        self.history_page.set_db(db)
        self.recommend_page.set_db(db)
        self.tip_page.set_db(db)
        self.annouce_page.set_db(db)

    def btn_event(self):
        self.btn_recommend.clicked.connect(lambda :self.to_page(0))
        self.btn_history.clicked.connect(lambda :self.to_page(1))
        self.btn_tip.clicked.connect(lambda :self.to_page(2))
        self.btn_announce.clicked.connect(lambda :self.to_page(3))

    def to_page(self,num):
        print('切换:',self.tool_list[num],'页')
        self.qsl.setCurrentIndex(num)
