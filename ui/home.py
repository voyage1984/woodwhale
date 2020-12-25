'''
    切换页面参考链接： https://zhuanlan.zhihu.com/p/61621705
    ---
    * 发送db到index        已完成
    * 登陆后显示个人头像
    * 登录后修改按键名称     已完成
    * 退出登录清除所有连接
'''

from PyQt5.QtWidgets import QWidget,QFrame,QPushButton,QVBoxLayout,QHBoxLayout,QStackedLayout,QLabel,QMessageBox
from PyQt5.QtGui import QIcon,QPixmap

from Login import LoginWindow as loginWindow
from ui.tools import tools
from ui.personal import personal as page_index
import MyDatabase

class Ui_home(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.db = MyDatabase.DBModel()
        self.mainwindow()
        self.rightwindow()
        self.leftwindow()
        self.click_event()

    def mainwindow(self):
        self.setWindowIcon(QIcon('./src/logo.ico'))
        self.setFixedSize(1280, 720)
        self.setWindowTitle('信息管理系统')
        self.layout = QHBoxLayout()
        # self.setStyleSheet('background-color:lightblue')

    def rightwindow(self):
        self.rightFrame = QFrame(self)
        # self.rightFrame.setStyleSheet('background-color:lightyellow')
        
        self.page1 = loginWindow()
        self.page2 = tools()
        self.page1_index = page_index()

        self.qsl = QStackedLayout(self.rightFrame)
        self.qsl.addWidget(self.page1)
        self.qsl.addWidget(self.page2)
        self.qsl.addWidget(self.page1_index)

    def leftwindow(self):
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('./src/logo.jpg'))
        self.label.setFixedSize(200, 200)

        self.btn_login = QPushButton('登录')
        self.btn_tools = QPushButton('工具箱')
        self.btn_book_management = QPushButton('图书管理')
        self.btn_user_management = QPushButton('用户管理')

        leftBox = QVBoxLayout()
        leftBox.addWidget(self.label)
        leftBox.addWidget(self.btn_login)
        leftBox.addWidget(self.btn_tools)
        leftBox.addWidget(self.btn_book_management)
        leftBox.addWidget(self.btn_user_management)

        self.layout.addLayout(leftBox)
        self.layout.addWidget(self.rightFrame)
        self.setLayout(self.layout)

    def click_event(self):
        self.page1._signal.connect(self.get_db)
        self.page1_index._signal.connect(self.logout)
        self.btn_login.clicked.connect(lambda :self.to_page(0))
        self.btn_tools.clicked.connect(lambda :self.to_page(1))


    def to_page(self,num):
        status = self.test_db()
        if num == 0:
            if status:
                self.qsl.setCurrentIndex(2)
            else:
                self.qsl.setCurrentIndex(0)
                self.btn_login.setText('登录')
        elif num == 1:
            if status:
                self.qsl.setCurrentIndex(1)
            else:
                self.login_Error()

    def get_db(self,db):
        print('已登录: home.get_db')
        self.db = db
        self.btn_login.setText('个人信息')
        self.qsl.setCurrentIndex(2)
        self.set_child_db()

    def set_child_db(self):
        self.page1_index.setdb(self.db)
        self.page2.setdb(self.db)

    def logout(self):
        print('登出: home.logout')
        self.db = None
        self.btn_login.setText('登录')
        self.qsl.setCurrentIndex(0)
        # self.set_child_db()

    def test_db(self):
        try:
            if self.db.status(0) != False:
                return True
            else:
                return False
        except:
            return False

    def login_Error(self):
        QMessageBox.warning(self, '错误！',
                                 "请先登录！", QMessageBox.Yes |
                                 QMessageBox.No, QMessageBox.No)

    def closeEvent(self,event):
        print('退出事件: home.Ui_home.closeEvent')
        reply = QMessageBox.question(self, '警告',
                                     "确认退出?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print('确认退出: home.Ui_home.closeEvent')
            event.accept()
        else:
            print('取消退出: home.Ui_home.closeEvent')
            event.ignore()
