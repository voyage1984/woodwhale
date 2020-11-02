from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QMessageBox
from PyQt5 import QtWidgets
import Login
import MyDatabase

class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MyDatabase.DBModel()

        self.VBoxLayout = QVBoxLayout()
        self.HBoxLayout = QHBoxLayout()
        self.btn_show = QtWidgets.QPushButton('查看')
        self.btn_login = QtWidgets.QPushButton('登录')
        self.textBrowser = QtWidgets.QTextBrowser()

        self.HBoxLayout.addWidget(self.btn_show)
        self.HBoxLayout.addWidget(self.btn_login)
        self.VBoxLayout.addLayout(self.HBoxLayout)
        self.VBoxLayout.addWidget(self.textBrowser)

        self.btn_login.clicked.connect(self.loginwindow)
        self.btn_show.clicked.connect(self.show_data)

        self.setLayout(self.VBoxLayout)

    # 登录成功
    def get_db(self,db):
        self.db = db
        self.btn_login.setText('登出')
        self.btn_login.clicked.connect(self.logoutwindow)

    # 登录窗口
    def loginwindow(self):
        self.login = Login.LoginWindow()
        self.login.show()
        self.login._signal.connect(self.get_db)

    # 登出窗口，默认登出，不显示
    def logoutwindow(self):
        print('登出...')
        self.db = None
        self.btn_login.setText('登录')
        self.btn_login.clicked.connect(self.loginwindow)

    # 查询数据
    def show_data(self):
        try:
            result = self.db.show_data()
            print('查询成功！: mainwindow.show_data')
        except:
            print('查询失败！: main.get_db')
            self.showError()
            return
        list = ''
        for i in result:
            list += str(i)
            list += ' '
        self.textBrowser.setText(list)


    # ‘查询’ 按钮错误事件
    def showError(self):
        print('查询错误: 未登录')
        QMessageBox.warning(self, '错误',
                            "请先登录！",
                            QMessageBox.Apply)