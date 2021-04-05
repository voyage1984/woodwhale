from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QPushButton,QFrame,QStackedLayout

from ui.book_pages import book_search
from ui import rent

from MyDatabase import DBModel

class book_manage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBModel()
        self.init()

    def init(self):
      self.btn_book_manage = QPushButton("图书管理")
      self.btn_rent_manage = QPushButton("借还管理")
      self.btn_rent_manage.setFixedSize(500,35)
      self.btn_book_manage.setFixedSize(500,35)
      self.btn_book_manage.clicked.connect(lambda :self.to_page(0))
      self.btn_rent_manage.clicked.connect(lambda :self.to_page(1))

      toolbar = QHBoxLayout()
      toolbar.addWidget(self.btn_book_manage)
      toolbar.addWidget(self.btn_rent_manage)

      self.search_page = book_search.book_search()
      self.rent_page = rent.rent()

      frame = QFrame(self)
      self.qsl = QStackedLayout(frame)
      self.qsl.addWidget(self.search_page)
      self.qsl.addWidget(self.rent_page)

      layout = QVBoxLayout()
      layout.addLayout(toolbar)
      layout.addWidget(frame)

      self.setLayout(layout)

    def setdb(self,db):
        self.db = db
        self.search_page.set_db(db)
        self.rent_page.set_db(db)

    def to_page(self,index):
        self.qsl.setCurrentIndex(index)