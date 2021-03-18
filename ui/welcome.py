from PyQt5.QtWidgets import QWidget,QHBoxLayout,QLabel
from PyQt5.QtCore import pyqtSignal,Qt
from PyQt5.QtGui import QPixmap, QFont

import MyDatabase

import System

class welcome(QWidget):
    _signal = pyqtSignal(MyDatabase.DBModel)
    def __init__(self):
        super().__init__()
        self.__init__gui()

    def set_username(self,username):
        self.username.setText(username)

    def __init__gui(self):
        self.whale = QLabel(self)
        # self.whale.setStyleSheet("background-color: rgb(250, 0, 0)")
        self.whale.setPixmap(QPixmap('./src/welcome.png'))
        self.whale.setFixedSize(1000,657)
        self.title = QLabel("欢迎使用木鲸图书馆管理系统")
        self.user = QLabel('当前登录用户：')
        self.username = QLabel('未知')

        self.user.setFixedSize(140,50)
        self.username.setFixedSize(160,50)
        self.user.setFont(QFont( "Microsoft YaHei", 15, 25))
        self.username.setFont(QFont( "Microsoft YaHei", 15, 25))

        self.user.setAlignment(Qt.AlignLeft)
        self.username.setAlignment(Qt.AlignLeft)

        mainframe = QHBoxLayout()
        rightframe = QHBoxLayout()
        mainframe.setAlignment(Qt.AlignTop)
        rightframe.setAlignment(Qt.AlignTop)

        rightframe.addWidget(self.user)
        rightframe.addWidget(self.username)

        mainframe.addWidget(self.whale)
        mainframe.addLayout(rightframe)

        self.setLayout(mainframe)

