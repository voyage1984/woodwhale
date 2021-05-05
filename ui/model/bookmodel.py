from PyQt5.Qt import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QVBoxLayout


class bookmodel(QWidget):
    def __init__(self,num,title,author,company,publish,bookmum):
        super().__init__()
        self.init(num,title,author,company,publish,bookmum)

    def init(self,num,title,author,company,publish,bookmum):
        label_id = QLabel(num)
        label_title = QLabel(title)
        label_author = QLabel(author)
        label_company = QLabel(company)
        label_publish = QLabel(publish)
        label_booknum = QLabel(bookmum)

        label_id.setFixedSize(50,30)
        label_title.setFixedSize(200,30)
        label_author.setFixedSize(150,30)
        label_company.setFixedSize(150,30)
        label_publish.setFixedSize(150,30)
        label_booknum.setFixedSize(150,30)

        label_id.setFont(QFont("Microsoft YaHei",10,QFont.Black))
        label_title.setFont(QFont("Microsoft YaHei",10,QFont.Black))
        label_author.setFont(QFont("Microsoft YaHei",10,QFont.Black))
        label_company.setFont(QFont("Microsoft YaHei",10,QFont.Black))
        label_publish.setFont(QFont("Microsoft YaHei",10,QFont.Black))
        label_booknum.setFont(QFont("Microsoft YaHei",10,QFont.Black))

        hlayout = QHBoxLayout()
        hlayout.addWidget(label_id)
        hlayout.addWidget(label_title)
        hlayout.addWidget(label_author)
        hlayout.addWidget(label_company)
        hlayout.addWidget(label_publish)
        hlayout.addWidget(label_booknum)
        hlayout.setAlignment(Qt.AlignTop)

        label_line = QLabel("")
        label_line.setFixedSize(900,1)
        label_line.setStyleSheet("background:transparent;border:2px solid black;")

        layout = QVBoxLayout()
        layout.addLayout(hlayout)
        layout.addWidget(label_line)


        self.setLayout(layout)
