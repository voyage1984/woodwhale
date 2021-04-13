from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QDialog, QTextEdit, QPushButton, QHBoxLayout, QLabel, QComboBox, \
    QListView

import System
from PyQt5.QtCore import pyqtSignal

class book_detail(QDialog):
        _signal = pyqtSignal()
        def __init__(self):
            super().__init__()
            self.db = None
            self.table = ''
            self.init()

        def init(self):
            self.setFixedSize(500, 400)
            setume = QLabel('编辑')
            self.status = QLabel('编辑中')
            labels = QHBoxLayout()
            labels.addWidget(setume)
            labels.addWidget(self.status)

            self.t_title = QLabel('图书名称：')
            self.title = QLineEdit()

            l_title = QHBoxLayout()
            l_title.addWidget(self.t_title)
            l_title.addWidget(self.title)

            self.t_author = QLabel('作者')
            self.author = QLineEdit()
            l_author = QHBoxLayout()
            l_author.addWidget(self.t_author)
            l_author.addWidget(self.author)

            self.t_company = QLabel('出版社')
            self.company = QLineEdit()
            l_company = QHBoxLayout()
            l_company.addWidget(self.t_company)
            l_company.addWidget(self.company)

            self.t_publish = QLabel('出版日')
            self.publish = QLineEdit()
            l_publish = QHBoxLayout()
            l_publish.addWidget(self.t_publish)
            l_publish.addWidget(self.publish)

            self.set_t_label(60,30)
            self.set_line_edit(250,30)

            buttons = QHBoxLayout()
            self.confirm = QPushButton('保存')
            self.delete = QPushButton('删除')
            buttons.addWidget(self.confirm)
            buttons.addWidget(self.delete)
            self.layout = QVBoxLayout()

            self.layout.addLayout(l_title)
            self.layout.addLayout(l_author)
            self.layout.addLayout(l_company)
            self.layout.addLayout(l_publish)
            self.tags_select()
            self.layout.addLayout(buttons)
            self.setLayout(self.layout)
            self.click_event()

        def set_line_edit(self,w,h):
            self.title.setFixedSize(w,h)
            self.author.setFixedSize(w,h)
            self.publish.setFixedSize(w,h)
            self.company.setFixedSize(w,h)

        def set_t_label(self,w,h):
            self.t_title.setFixedSize(w, h)
            self.t_author.setFixedSize(w, h)
            self.t_company.setFixedSize(w, h)
            self.t_publish.setFixedSize(w, h)

        def set_content(self,id):
            print('开始显示detail...')
            self.status.setText('编辑中')
            self.id = id
            print('id is :',self.id)
            self.setWindowTitle(id)
            self.list = self.db.get_search_from_table(0,self.id,'booklist',1)
            print('获取成功！')
            self.title.setText(str(self.list[0][1]).strip())
            self.author.setText(self.list[0][2].strip())
            self.company.setText(self.list[0][3].strip())
            self.publish.setText(str(self.list[0][4]).strip())
            self.menus.addItem(self.list[0][5])
            self.menus2.addItem(self.list[0][6])
            self.set_tags()

        def click_event(self):
            self.confirm.clicked.connect(self.save_event)
            self.delete.clicked.connect(self.delete_event)

        def save_event(self):
            print('开始保存',System.func_name())
            title = self.title.text()
            author = self.author.text()
            company = self.company.text()
            publish = self.publish.text()
            if (len(title) == 0 or len(author) == 0 or len(company) == 0 or len(publish) == 0):
                System.dialog(self, '错误', '内容不能为空！')
                return
            try:
                tag1 = self.menus.currentText()
                tag2 = self.menus2.currentText()
                print("设置tag：",tag1,",",tag2)
                if self.db.update_book(self.table,self.id,title,author,company,publish,tag1,tag2):
                    self.status.setText('已保存')
                    self.close()
                    self._signal.emit()
                else:
                    System.dialog(self,'保存失败！','请稍后再试')
            except Exception as e:
                print('错误',e)

        def delete_event(self):
            print('删除事件')
            if(self.list[0][7]!=self.list[0][8]):
                System.dialog(self,"错误！","此书库存与总数不匹配："+str(self.list[0][7])+"/"+str(self.list[0][8])+"\n无法删除")
                return
            if System.dialog(self,'警告','确认删除？'):
                print('确认删除')
                if self.db.delete_data(self.table,"id",self.id):
                    print('已删除数据：',self.id)
                    self.close()
                    self._signal.emit()
                else:
                    System.dialog(self,'删除失败！','请稍后再试')
                    print('删除失败')
            else:
                print('取消删除')

        def set_db(self,db,table):
            self.db = db
            self.table = table

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
            self.taglist = self.db.get_all_from_table('taglist')
            if self.taglist == False:
                System.dialog(self, "连接数据库失败！", "请稍后再试")
                return
            self.menus.clear()
            self.menus.addItem(self.list[0][5])
            for line in self.taglist:
                self.menus.addItem(line[1])
            self.menus.currentIndexChanged.connect(self.set_tag2)

        def set_tag2(self):
            self.menus2.clear()
            index = self.menus.currentIndex()
            if index == 0:
                self.menus2.addItem(self.list[0][6])
            else:
                list = self.taglist[index-1][2]
                list = System.parsing(list.strip(),' ')
                # self.menus2.setMaxVisibleItems(len(list))
                for item in list:
                    self.menus2.addItem(item)


