'''
    登录窗口
    待办：
        1. 布局美化
        2. 字体设置
        3. 明文密码切换
        4. 登录状态判断(弹窗提示)      已完成
        5. 接入数据库                已完成
        6. 传递db到主窗口             已完成
'''

from PyQt5.QtWidgets import QWidget,QPushButton,QMessageBox,\
    QHBoxLayout,QVBoxLayout,QLabel,QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

import MyDatabase

class LoginWindow(QWidget):
    _signal = pyqtSignal(MyDatabase.DBModel)
    def __init__(self):
        super().__init__()
        self.__init__gui()

    # 窗口设置
    def __init__gui(self):
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon('./src/logo.ico'))
        self.setInput()
        self.setBtn()
        self.win = QVBoxLayout()
        self.win.addItem(self.inputs)
        self.win.addItem(self.btns)
        self.setLayout(self.win)

    # 输入框
    def setInput(self):
        self.lab_username = QLabel('用户名：')
        self.lab_password = QLabel('密  码：')
        self.edit_username = QLineEdit()
        self.edit_password = QLineEdit()

        self.edit_password.setText("password")
        self.edit_username.setText("username")

        self.username = QHBoxLayout()
        self.password = QHBoxLayout()
        self.username.addWidget(self.lab_username)
        self.username.addWidget(self.edit_username)
        self.password.addWidget(self.lab_password)
        self.password.addWidget(self.edit_password)
        self.inputs = QVBoxLayout()
        self.inputs.addItem(self.username)
        self.inputs.addItem(self.password)

    # 按钮框：确认 / 取消
    def setBtn(self):
        self.btn_login  = QPushButton('登录',self)
        self.btn_login.resize(self.btn_login.sizeHint())
        self.btns = QHBoxLayout()
        self.btns.addWidget(self.btn_login)

        self.btn_login.clicked.connect(self.confirmEvent)

    # 登录事件
    def confirmEvent(self):
        name = self.edit_username.text()
        password = self.edit_password.text()

        if len(name)==0 or len(password)==0:
           print('账号 / 密码不能为空！: Login.confirmEvent')
           self.nonEmpty()
        else:                           # 接入数据库
            print('正在登录: Login.LoginWindow.confirmEvent')
            try:
                self.Login(name,password)
            except:
                print('登录失败！: Login.confirmEvent')

    # 登录数据库
    def Login(self,name,password):
        self.db = MyDatabase.DBModel()
        if self.db.conn(name,password) == False:
            print('登录错误！: Login.LoginWindow.Login')
            self.loginError()
            return False
        else:
            print('登录成功!: Login.LoginWindow.Login')
            self._signal.emit(self.db)
            self.close()


    # 登录失败提示框
    def loginError(self):
        print('登录失败!: Login.LoginWindow.loginError')
        QMessageBox.warning(self, '错误',
                            "用户名 / 密码错误！",
                            QMessageBox.Apply)

    # 判断输入是否为空
    def nonEmpty(self):
        print('登录失败!: Login.LoginWindow.nonEmpty')
        QMessageBox.warning(self,'错误',
                                 "用户名 / 密码不能为空！",
                                 QMessageBox.Apply)

    # 取消事件
    def closeEvent(self, event):
        print('取消事件: Login.LoginWindow.LogincloseEvent')
        try:
            if self.db.status(0) != False:
                print('登录成功！: Login.LoginWindow.Login.closeEvent')
            else:
                print('登录失败！: Login.LoginWindow.Login.closeEvent')
        except:
            print('登录失败！: Login.LoginWindow.Login.closeEvent')

