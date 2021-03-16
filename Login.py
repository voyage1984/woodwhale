from PyQt5.QtWidgets import QWidget,QPushButton,QMessageBox,\
    QHBoxLayout,QVBoxLayout,QLabel,QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

import MyDatabase

import System

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

        self.edit_password.setText(System.password)
        self.edit_username.setText(System.username)

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
        funcname = System.func_name()

        if len(name)==0 or len(password)==0:
           print('账号 / 密码不能为空！')
           self.nonEmpty()
        else:                           # 接入数据库
            print('正在登录',funcname)
            try:
                self.Login(name,password)
            except:
                print('登录失败！',funcname)

    # 登录数据库
    def Login(self,name,password):
        self.db = MyDatabase.DBModel()
        System.func_name()
        if self.db.conn(name,password) == False:
            print('登录错误！',System.func_name())
            self.loginError()
            return False
        else:
            print('登录成功!',System.func_name())
            self._signal.emit(self.db)
            self.close()


    # 登录失败提示框
    def loginError(self):
        print('登录失败!',System.func_name())
        QMessageBox.warning(self, '错误',
                            "请检查用户名/密码！",
                            QMessageBox.Apply)

    # 判断输入是否为空
    def nonEmpty(self):
        print('登录失败!',System.func_name())
        QMessageBox.warning(self,'错误',
                                 "用户名 / 密码不能为空！",
                                 QMessageBox.Apply)

    # 取消事件
    def closeEvent(self, event):
        print('取消事件',System.func_name())
        try:
            if self.db.status(0) != False:
                print('登录成功！',System.func_name())
            else:
                print('登录失败！',System.func_name())
        except:
            print('登录失败！',System.func_name())

