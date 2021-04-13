import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel, QListView

from MyDatabase import DBModel

import System

class rent(QWidget):
    count = 5
    borrow = 0
    rentlist = None

    def __init__(self):
        super().__init__()
        self.db = DBModel()
        self.init()

    def set_db(self,db):
        self.db = db

    def init(self):
        self.init_labels()
        self.user_menus = QComboBox()
        self.user_menus.setView(QListView())
        self.user_menus.setStyleSheet("QComboBox QAbstractItemView::item {min-height: 25px;}")
        self.user_menus.setFixedSize(100, 35)
        self.user_menus.addItem("用户ID")
        self.user_menus.addItem("用户姓名")
        self.input_user = QLineEdit()
        self.btn_search_user = QPushButton("查询")
        layout_user_search = QHBoxLayout()
        layout_user_search.addWidget(self.user_menus)
        layout_user_search.addWidget(self.input_user)
        layout_user_search.addWidget(self.btn_search_user)

        layout_user_info = QVBoxLayout()
        layout_user_info.setSpacing(40)
        layout_user_info.setAlignment(Qt.AlignTop)
        layout_user_info.addLayout(layout_user_search)
        layout_user_info.addWidget(self.user_id)
        layout_user_info.addWidget(self.user_name)
        layout_user_info.addWidget(self.rent_rest)
        layout_user_search.setSpacing(10)
        layout_user_search.setAlignment(Qt.AlignLeft)


        bookmenu = QComboBox()
        bookmenu.addItem("ID")
        bookmenu.setFixedSize(50, 35)
        self.book_info = QLineEdit()
        self.btn_search_book = QPushButton("查询图书")
        layout_book_search = QHBoxLayout()
        layout_book_search.addWidget(bookmenu)
        layout_book_search.addWidget(self.book_info)
        layout_book_search.addWidget(self.btn_search_book)

        layout_book_info = QVBoxLayout()
        layout_book_info.setContentsMargins(30,0,0,10)
        layout_book_info.setAlignment(Qt.AlignTop)
        layout_book_info.setSpacing(40)
        layout_book_info.addLayout(layout_book_search)
        layout_book_info.addWidget(self.book_id)
        layout_book_info.addWidget(self.book_name)
        layout_book_info.addWidget(self.book_author)
        layout_book_info.addWidget(self.book_num)
        layout_book_info.addWidget(self.book_rest)
        layout_book_info.addWidget(self.book_rent)
        layout_book_info.addWidget(self.book_return)

        self.btn_rent = QPushButton("借出")
        self.btn_return = QPushButton("归还")
        self.btn_rent.setFixedSize(100,40)
        self.btn_return.setFixedSize(100,40)
        layout_operation = QVBoxLayout()
        layout_operation.addWidget(self.btn_rent)
        layout_operation.addWidget(self.btn_return)

        layout = QHBoxLayout()
        layout.addLayout(layout_user_info)
        layout.addLayout(layout_book_info)
        layout.addLayout(layout_operation)
        self.setLayout(layout)
        self.init_btns()

    def init_labels(self):
        self.user_name = QLabel("用户姓名：")
        self.user_id = QLabel("用户ID：")
        self.rent_rest = QLabel("可借书数：")
        self.book_id = QLabel("图书ID：")
        self.book_name = QLabel("图书标题：")
        self.book_author = QLabel("作者：")
        self.book_num = QLabel("索书号：")
        self.book_rest = QLabel("在库：")
        self.book_rent = QLabel("借出日期：")
        self.book_return = QLabel("归还期限：")
        self.setStyleSheet('QLabel{font-size:14px}')

    def init_btns(self):
        self.btn_search_user.clicked.connect(self.get_user)
        self.btn_search_book.clicked.connect(self.get_book)
        self.btn_rent.clicked.connect(self.rent_book)
        self.btn_return.clicked.connect(self.return_book)
        self.btn_search_book.setEnabled(0)
        self.btn_rent.setEnabled(0)
        self.btn_return.setEnabled(0)

    def get_user(self):
        self.renew_labels()
        self.btn_rent.setEnabled(0)
        self.btn_return.setEnabled(0)
        self.count = 5
        print("开始查询")
        user = self.input_user.text()
        if len(user)==0:
            System.dialog(self,"错误!","用户信息不能为空值")
            return
        print("获取用户：",user)
        index = self.user_menus.currentIndex()
        print("获取索引：", index)

        if index == 0:
            col = "id"
        elif index == 1:
            col = "username"
        else:
            System.dialog(self,"发生了错误","获取索引出错:"+index)
            return
        userinfo = self.db.get_search_from_table(col,user,"userlist",1)
        if(len(userinfo)==0):
            System.dialog(self,"获取用户失败！","未查询到用户："+user)
            self.btn_search_book.setEnabled(0)
            return
        self.btn_search_book.setEnabled(1)
        self.userlist = []
        for item in userinfo[0]:
            print(item)
            self.userlist.append(str(item).strip())

        print("解析数据成功！")
        print("设置用户id：",self.userlist[0])
        self.user_id.setText("用户ID："+self.userlist[0])
        print("设置用户姓名：", self.userlist[1])
        self.user_name.setText("用户姓名："+self.userlist[1])
        for i in range(5,10):
            if(self.userlist[i]=='0'):
                pass
            else:
                self.count-=1

        print("设置可借书数：", self.count)
        self.rent_rest.setText("可借书数："+str(self.count))

    def get_book(self):
        book = self.book_info.text()
        if(len(book)==0):
            System.dialog(self,"错误！","图书id不能为空")
            return
        bookinfo = self.db.get_search_from_table(0,book,"booklist",1)
        if(len(bookinfo)==0):
            System.dialog(self,"错误！","获取图书失败！"+book)
            return
        self.booklist = []
        for item in bookinfo[0]:
            print(item)
            self.booklist.append(str(item).strip())
        self.set_opration_btns()
        self.book_id.setText("图书ID："+self.booklist[0])
        self.book_name.setText("图书标题："+self.booklist[1])
        self.book_author.setText("作者："+self.booklist[2])
        self.book_num.setText("索书号："+self.booklist[9])
        self.book_rest.setText("在库："+self.booklist[7])
        self.get_book2()

    def get_book2(self):
        print("借阅表：",self.rentlist)
        if (self.rentlist==None or len(self.rentlist) == 0):
            print("获取错误！")
            self.book_rent.setText("借出日期：")
            self.book_return.setText("归还期限：")
            return

        times = System.parsingdate(str(self.rentlist[0][4]))
        self.rentid = self.rentlist[0][0]
        rentday = "self.rentlist[0][3]"
        returnday = self.rentlist[0][4]
        for i in self.rentlist:
            print("获取日期")
            timenow = System.parsingdate(str(i[4]))
            if times > timenow:
                times = timenow
                self.rentid = i[0]
                rentday = i[3]
                returnday = i[4]
        print(self.rentid)
        print(rentday,returnday)
        self.book_rent.setText("借出日期：" + str(rentday))
        if System.parsingdate(str(returnday))<System.parsingdate(str(time.strftime('%Y-%m-%d', time.localtime(time.time() + 30 * 24 * 3600)))):
            self.book_return.setText("归还期限：" + str(returnday) + "[已超期！]")
        else:
            self.book_return.setText("归还期限：" + str(returnday))


    def set_opration_btns(self):
        self.rentlist = None
        self.btn_return.setEnabled(0)
        self.btn_rent.setEnabled(0)
        # 借书条件
        """如果书库存<=0或者用户可借书数<=0，不能借书"""
        if (int(self.booklist[7]) <= 0 or self.count<=0):
            self.btn_rent.setEnabled(0)
        else:
            self.btn_rent.setEnabled(1)
        """还书条件: 用户借阅表里有这本书"""
        for i in range(5,10):
            if self.booklist[0] == self.userlist[i]:
                print("图书："+self.booklist[0]+"已被此用户借阅")
                self.rentlist = self.db.get_search_from_table2("rentlist","userid",self.userlist[0],"bookid",self.booklist[0])
                self.btn_return.setEnabled(1)
                self.borrow = i
                return


    def rent_book(self):
        num = int(self.booklist[7])-1
        if(num<0):
            System.dialog(self, "借书失败！", "在库小于0！请联系管理员核实数据!")
            return
        for i in range(5, 10):
            if (self.userlist[i] == '0'):
                borrow = "borrow"+str(i-4)
                if self.db.update_table("userlist",borrow,self.booklist[0],"id",self.userlist[0]):
                    if self.db.update_table("booklist","rest",str(num),"id",self.booklist[0]):
                        if self.db.insert_rent(self.userlist[0],self.booklist[0]):
                            System.dialog(self,"借出成功！","已借出："+self.userlist[1]+":"+self.booklist[1])
                            self.renew_labels()
                            return
                    else:
                        System.dialog(self, "更新在库失败！", "请联系管理员核查数据！")
                        return
                else:
                    System.dialog(self, "借书失败！", "请重试")
                    return

    def return_book(self):
        colName = "borrow"+str(self.borrow-4)
        rest = int(self.booklist[7])+1
        if rest > int(self.booklist[8]):
            System.dialog(self, "库存超过总数！", "请联系管理员核实数据")
            return

        if(self.db.update_table("userlist",colName,"0","id",self.userlist[0])):
            if(self.db.update_table("booklist","rest",str(rest),"id",self.booklist[0])):
                print("test")
                if(self.db.delete_data("rentlist","id",str(self.rentid))):
                    System.dialog(self,"还书成功！","用户："+self.userlist[1])
                    self.renew_labels()
            else:
                System.dialog(self, "更新在库失败！", "请联系管理员核查数据！")
        else:
            System.dialog(self,"还书失败！","请重试")

    def renew_labels(self):
        self.user_name.setText("用户姓名：")
        self.user_id.setText("用户ID：")
        self.rent_rest.setText("可借书数：")
        self.book_id.setText("图书ID：")
        self.book_name.setText("图书标题：")
        self.book_author.setText("作者：")
        self.book_num.setText("索书号：")
        self.book_rest.setText("在库：")
        self.book_rent.setText("借出日期：")
        self.book_return.setText("归还期限：")
        self.btn_rent.setEnabled(0)
        self.btn_return.setEnabled(0)
        self.btn_search_book.setEnabled(0)