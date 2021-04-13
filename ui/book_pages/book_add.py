from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QLineEdit, QTextEdit, QVBoxLayout, QPushButton, QComboBox, \
    QListView
from PyQt5.QtCore import QThread, pyqtSignal

import MyDatabase
import System


class book_add(QWidget):
    def __init__(self):
        self.db = MyDatabase.DBModel()
        super().__init__()
        self.init()

    def set_db(self, db):
        self.db = db

    def init(self):
        label_title = QLabel('标题：')
        label_author = QLabel('作者：')
        label_company = QLabel('出版社：')
        label_publish = QLabel('出版时间：')
        label_total= QLabel('总数：')
        label_booknum = QLabel('索书号：')

        label_title.setFixedSize(100, 40)
        label_author.setFixedSize(100, 40)
        label_company.setFixedSize(100, 40)
        label_publish.setFixedSize(100, 40)
        label_total.setFixedSize(100, 40)
        label_booknum.setFixedSize(100, 40)

        self.input_author = QLineEdit()
        self.input_title = QLineEdit()
        self.input_publsh = QLineEdit()
        self.input_company = QLineEdit()
        self.input_total = QLineEdit()
        self.input_booknum = QLineEdit()

        self.input_title.setFixedSize(250,30)
        self.input_author.setFixedSize(250,30)
        self.input_publsh.setFixedSize(250,30)
        self.input_company.setFixedSize(250,30)
        self.input_total.setFixedSize(250,30)
        self.input_booknum.setFixedSize(250,30)
        self.input_total.setValidator(QIntValidator(1,100))

        self.submit_button = QPushButton('插入')
        self.submit_button.clicked.connect(self.submit_event)

        layout_author = QHBoxLayout()
        layout_title = QHBoxLayout()
        layout_company = QHBoxLayout()
        layout_publish = QHBoxLayout()
        layout_total = QHBoxLayout()
        layout_booknum = QHBoxLayout()

        layout_title.addWidget(label_title)
        layout_title.addWidget(self.input_title)
        layout_author.addWidget(label_author)
        layout_author.addWidget(self.input_author)
        layout_company.addWidget(label_company)
        layout_company.addWidget(self.input_company)
        layout_publish.addWidget(label_publish)
        layout_publish.addWidget(self.input_publsh)
        layout_total.addWidget(label_total)
        layout_total.addWidget(self.input_total)
        layout_booknum.addWidget(label_booknum)
        layout_booknum.addWidget(self.input_booknum)


        self.layout = QVBoxLayout()
        self.layout.addLayout(layout_title)
        self.layout.addLayout(layout_author)
        self.layout.addLayout(layout_company)
        self.layout.addLayout(layout_publish)
        self.layout.addLayout(layout_total)
        self.layout.addLayout(layout_booknum)

        self.tags_select()

        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

    def submit_event(self):
        if self.db.status(0) != False:
            self.insert_data()
        else:
            print('连结数据库错误!', System.func_name())

    def insert_data(self):
        print('开始插入数据', System.func_name())
        list = []
        list.append(self.input_title.text())
        list.append(self.input_author.text())
        list.append(self.input_company.text())
        list.append(self.input_publsh.text())
        list.append(self.input_total.text())
        list.append(self.input_booknum.text())
        check = self.check_input(list)
        if check == False:
            return
        else:
            if self.db.insert_book(list) == True:
                print('添加成功！')
                System.dialog(self, '添加成功', "添加成功！"+list[0])
                self.clear_text()
            else:
                print('添加失败！', System.func_name())
                System.dialog(self, '插入失败！', "请检查输入")

    def check_input(self,list):
        for item in list:
            if len(item) == 0:
                System.dialog(self,"存在空值","请检查输入")
                return False
        if self.menus.currentIndex() == 0:
            System.dialog(self, "请选择图书类别", "选择图书类别")
            return False
        list.append(self.menus.currentText())
        list.append(self.menus2.currentText())
        return True

    def clear_text(self):
        self.input_title.setText("")
        self.input_author.setText("")
        self.input_company.setText("")
        self.input_publsh.setText("")
        self.input_booknum.setText("")
        self.input_total.setText('')
        self.menus.setCurrentIndex(0)

    def tags_select(self):
        self.menus = QComboBox()
        self.menus2 = QComboBox()
        self.menus.setView(QListView())
        self.menus.setStyleSheet("QComboBox QAbstractItemView::item {min-height: 25px;}")
        self.menus2.setView(QListView())
        self.menus2.setStyleSheet("QComboBox QAbstractItemView::item {min-height: 25px;}")
        self.menus.setFixedSize(150, 35)
        self.menus2.setFixedSize(150, 35)
        menus = QHBoxLayout()
        menus.addWidget(self.menus)
        menus.addWidget(self.menus2)
        self.layout.addLayout(menus)

    def set_tags(self):
        self.list = self.db.get_all_from_table('taglist')
        if self.list == False:
            System.dialog(self, "连接数据库失败！", "请稍后再试")
            return
        self.menus.clear()
        self.menus.addItem("")
        # self.menus.setMaxVisibleItems(len(self.list))
        for line in self.list:
            self.menus.addItem(line[1])
        self.menus.currentIndexChanged.connect(self.set_tag2)

    def set_tag2(self):
        print('开始设置tag2')
        self.menus2.clear()
        index = self.menus.currentIndex()
        if index == 0:
            return
        list = self.list[index-1][2]
        list = System.parsing(list.strip(),' ')
        # self.menus2.setMaxVisibleItems(len(list))
        for item in list:
            self.menus2.addItem(item)





