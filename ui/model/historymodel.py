from PyQt5.Qt import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QVBoxLayout


class historymodel(QWidget):
    def __init__(self,num,title,author):
        super().__init__()
        self.init(num,title,author)

    def init(self,num,title,author):
        label_id = QLabel(num)
        label_title = QLabel(title)

        label_author = QLabel(author)
        label_id.setFixedSize(100,30)
        label_title.setFixedSize(300,30)
        label_author.setFixedSize(350,30)

        label_id.setFont(QFont("Microsoft YaHei",10,QFont.Black))
        label_title.setFont(QFont("Microsoft YaHei",10,QFont.Black))
        label_author.setFont(QFont("Microsoft YaHei",10,QFont.Black))

        hlayout = QHBoxLayout()
        hlayout.addWidget(label_id)
        hlayout.addWidget(label_title)
        hlayout.addWidget(label_author)
        hlayout.setAlignment(Qt.AlignTop)

        label_line = QLabel("")
        label_line.setFixedSize(750,1)
        label_line.setStyleSheet("background:transparent;border:2px solid black;")

        layout = QVBoxLayout()
        layout.addLayout(hlayout)
        layout.addWidget(label_line)


        self.setLayout(layout)
