import datetime

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout,QVBoxLayout,QLineEdit,QPushButton,QTextEdit
from  PyQt5.QtCore import Qt

from ui.recommend_pages import recomment_result
import System

class recommend(QWidget):
    def __init__(self,table):
        self.table = table
        super().__init__()
        self.init()

    def set_db(self,db):
        self.db = db
        self.result.set_db(db)
        self.result.get_data()

    def init(self):
        self.db = None
        self.leftFrame()
        self.rightFrame()
        self.win = QHBoxLayout()
        self.win.addLayout(self.left)
        self.win.addLayout(self.right)
        self.setLayout(self.win)

        self.btn_add.clicked.connect(self.add_recommend)

    def leftFrame(self):
        self.label_search = QLabel('搜索标题:')
        self.label_search.setFont(QFont("Microsoft YaHei", 10, 25))
        self.edit_serach =  QLineEdit()
        self.btn_search = QPushButton('搜索')
        search_bar = QHBoxLayout()
        search_bar.addWidget(self.label_search)
        search_bar.addWidget(self.edit_serach)
        search_bar.addWidget(self.btn_search)

        self.btn_search.clicked.connect(self.search)

        self.result = recomment_result.recommend_result(self.table)
        self.left = QVBoxLayout()
        self.left.addLayout(search_bar)
        self.left.addWidget(self.result)

    def rightFrame(self):
        self .label_add = QLabel('新建'+self.table)
        self.label_title = QLabel('标题：')
        self.label_article = QLabel('正文：')
        self.label_add.setFont(QFont("Microsoft YaHei", 15, 55))
        self.label_title.setFont(QFont("Microsoft YaHei", 12, 55))
        self.label_article.setFont(QFont("Microsoft YaHei", 12, 55))

        self.edit_title = QLineEdit()
        self.edit_article = QTextEdit()

        title_bar = QHBoxLayout()
        title_bar.addWidget(self.label_title)
        title_bar.addWidget(self.edit_title)
        article_bar = QHBoxLayout()
        article_bar.addWidget(self.label_article)
        article_bar.addWidget(self.edit_article)
        self.label_article.setAlignment(Qt.AlignTop)

        self.btn_add = QPushButton('新建')
        self.right = QVBoxLayout()
        self.right.addWidget(self.label_add)
        self.right.addLayout(title_bar)
        self.right.addLayout(article_bar)
        self.right.addWidget(self.btn_add)
        self.right.setContentsMargins(20,0,0,0)

    def add_recommend(self):
        print('添加recommend')
        # date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        title = self.edit_title.text()
        article = self.edit_article.toPlainText()
        if(len(title)==0 or len(article)==0):
            System.dialog(self,'错误','内容不能为空！')
            return
        if self.db.insert_tdta(self.table,None,title,article) == False:
            print('提交失败！')
        else:
            print('提交成功！')
            self.edit_title.setText('')
            self.edit_article.setText('')
            self.result.renew_item()

    def search(self):
        content = self.edit_serach.text()
        print('搜索内容：',content)
        if len(content) == 0:
            print('搜索内容为空，默认全局搜索')
            self.result.get_data()
            return
        else:
            self.result.set_data(content)



