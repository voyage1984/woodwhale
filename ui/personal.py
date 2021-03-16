from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QMessageBox
# from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
import MyDatabase
import System

class personal(QWidget):
    _signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.db = MyDatabase.DBModel()

        self.VBoxLayout = QVBoxLayout()
        self.HBoxLayout = QHBoxLayout()
        self.btn_show = QtWidgets.QPushButton('个人信息')
        self.btn_login = QtWidgets.QPushButton('登出')
        self.textBrowser = QtWidgets.QTextBrowser()

        self.HBoxLayout.addWidget(self.btn_show)
        self.HBoxLayout.addWidget(self.btn_login)
        self.VBoxLayout.addLayout(self.HBoxLayout)
        self.VBoxLayout.addWidget(self.textBrowser)

        self.btn_login.clicked.connect(self.logoutwindow)
        self.btn_show.clicked.connect(self.showdata)

        self.setLayout(self.VBoxLayout)

    def setdb(self,db):
        self.db = db
        r1 = db.get_user()
        r ='当前登录用户: ' + str(r1)
        print(r)
        self.textBrowser.setText(r)

    # 登出窗口，默认登出，不显示
    def logoutwindow(self):
        print('登出')
        self.db = None
        self.btn_login.setText('登录')
        self._signal.emit()

    # 查询数据
    def showdata(self):
        try:
            result = self.db.show_data('userlist')
            print('查询成功')
        except:
            print('查询失败！',System.func_name())
            self.showError()
            return
        list = ''
        for i in result:
            list += str(i)
            list += ' '
        self.textBrowser.setText(list)


    # ‘查询’ 按钮错误事件
    def showError(self):
        print('查询错误！')
        QMessageBox.warning(self, '错误',
                            "读取失败！",
                            QMessageBox.Apply)