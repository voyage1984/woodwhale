'''
    切换页面参考链接： https://zhuanlan.zhihu.com/p/61621705
    ---
    * 发送db到index
    * 登陆后显示个人头像
    * 登录后修改按键名称
'''

from PyQt5.QtWidgets import QWidget,QFrame,QPushButton,QVBoxLayout,QHBoxLayout,QStackedLayout,QLabel,QMessageBox
from PyQt5.QtGui import QIcon,QPixmap

import Login
from ui.page2 import page2
from ui.personal import personal as page_index
import MyDatabase

class Ui_home(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.db = MyDatabase.DBModel()

        self.mainwindow()           # 绘制主窗口
        self.rightwindow()          # 绘制右半部分
        self.leftwindow()           # 绘制左半部分

    def mainwindow(self):           # 主窗口
        self.setWindowIcon(QIcon('./src/logo.ico'))     # 窗口图标
        self.setFixedSize(1280, 720)                    # 固定窗口大小
        self.setWindowTitle('信息管理系统')               # 窗口标题
        self.layout = QHBoxLayout()                     # 窗口容器
        self.setStyleSheet('background-color:lightblue')    # 窗口样式

    def rightwindow(self):                              # 右窗口
        self.rightFrame = QFrame(self)                  # 右窗口类型
        self.rightFrame.setStyleSheet('background-color:lightyellow')

        self.qsl = QStackedLayout(self.rightFrame)      # 用于切换子窗口
        self.page1 = Login.LoginWindow()                # 用于切换的子窗口，登录页
        self.page2 = page2()                            # 用于切换的子窗口，测试页
        self.page1_index = page_index()                 # 用于切换的子窗口，登录成功页

        self.page1._signal.connect(self.get_db)         # 定义信号哦
        self.page1_index._signal.connect(self.logout)

        self.qsl.addWidget(self.page1)
        self.qsl.addWidget(self.page2)
        self.qsl.addWidget(self.page1_index)

    def leftwindow(self):                               # 左窗口
        self.label = QLabel(self)                       # 用于显示图片的label
        self.label.setPixmap(QPixmap('./src/logo.jpg')) # 图片地址
        self.label.setFixedSize(200, 200)               # 显示区域大小

        self.btn_login = QPushButton('登录')             # 按钮
        self.btn_search = QPushButton('查询')

        self.btn_login.clicked.connect(self.setpage1)   # 绑定事件
        self.btn_search.clicked.connect(self.setpage2)

        self.leftBox = QVBoxLayout()                    # 排版按钮与图标
        self.leftBox.addWidget(self.label)
        self.leftBox.addWidget(self.btn_login)
        self.leftBox.addWidget(self.btn_search)

        self.layout.addLayout(self.leftBox)
        self.layout.addWidget(self.rightFrame)
        self.setLayout(self.layout)

    def get_db(self,db):                                # 登录成功事件
        print('已登录: home.get_db')
        self.db = db                                    # 获取db
        self.page1_index.setdb(db)                      # 传送db到子窗口：登录成功页
        self.btn_login.setText('个人信息')               # 改变按钮显示
        self.qsl.setCurrentIndex(2)                     # 改变当前页面：登录页 -> 登录成功页

    def logout(self):                                   # 登出事件
        print('登出: home.logout')
        self.db = None                                  # 舍弃数据库连接
        self.btn_login.setText('登录')                   # 更改按钮显示
        self.qsl.setCurrentIndex(0)                     # 改变当前页面：登录成功页 -> 登录页

    def setpage1(self):                                 # 切换page1
        print('切换page1')
        try:                                            # 根据db状态判断打开哪个页面
            if self.db.status() != False:
                self.qsl.setCurrentIndex(2)
            else:
                self.qsl.setCurrentIndex(0)
                self.btn_login.setText('登录')
        except:                                         # db不存在
            self.qsl.setCurrentIndex(0)

    def setpage2(self):                                 # 切换page2
        print('切换page2')
        self.qsl.setCurrentIndex(1)

    def closeEvent(self,event):
        reply = QMessageBox.question(self, '警告',
                                     "确认退出?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
